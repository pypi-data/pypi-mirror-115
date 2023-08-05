from typing import Type, List

from AoE2ScenarioParser.helper.exceptions import UnsupportedAttributeError
from AoE2ScenarioParser.objects.aoe2_object import AoE2Object
from AoE2ScenarioParser.sections.aoe2_file_section import AoE2FileSection
from AoE2ScenarioParser.sections.dependencies.dependency import handle_retriever_dependency
from AoE2ScenarioParser.sections.retrievers.support import Support


class RetrieverObjectLink:
    def __init__(self,
                 variable_name: str,
                 section_name: str = None,
                 link: str = None,
                 support: Support = None,
                 process_as_object: Type[AoE2Object] = None,
                 retrieve_instance_number: bool = False,
                 retrieve_history_number: int = -1
                 ):
        if sum([link is not None, retrieve_instance_number, (retrieve_history_number != -1)]) != 1:
            raise ValueError("You must use exactly one of 'link' and the two 'retrieve...number' parameters.")

        self.name: str = variable_name
        self.section_name = section_name
        self.link = link
        self.support: Support = support
        self.is_special_unit_case = self._is_special_unit_case()
        self.process_as_object: Type[AoE2Object] = process_as_object
        self.retrieve_instance_number: bool = retrieve_instance_number
        self.retrieve_history_number: int = retrieve_history_number

        self.splitted_link: List[str] = link.split('.') if link is not None else []

    def construct(self, sections, scenario_version, number_hist=None):
        if number_hist is None:
            number_hist = []
        instance_number = AoE2Object.get_instance_number(number_hist=number_hist)

        if self.retrieve_instance_number:
            return instance_number
        elif self.retrieve_history_number != -1:
            return number_hist[self.retrieve_history_number]
        else:
            if self.is_special_unit_case:
                return self._construct_special_unit_case(sections, scenario_version)

            # Retrieve value without using eval() -- Eval is slow
            value = sections[self.section_name]
            for index, item in enumerate(self.splitted_link):
                try:
                    if "[" in item:
                        value = getattr(value, item[:-11])[number_hist[index]]
                    else:
                        value = getattr(value, item)
                except AttributeError as e:
                    # Maybe not supported in current version. if actually not supported -> ignore
                    if self.support is not None:
                        if not self.support.supports(scenario_version):
                            value = None
                            break
                    raise e

            if self.process_as_object:
                return self.process_object_list(value, number_hist, sections, scenario_version)
            return value

    def process_object_list(self, value_list, instance_number_history, sections, scenario_version):
        object_list = []
        for index, struct in enumerate(value_list):
            object_list.append(
                self.process_as_object._construct(scenario_version, sections, instance_number_history + [index])
            )
        return object_list

    def commit(self, sections, scenario_version, host_obj: AoE2Object):
        # Object-only attributes for the ease of access of information.
        # Not actually representing a value in the scenario file.
        if self.retrieve_instance_number or self.retrieve_history_number >= 0:
            return

        number_hist = host_obj._instance_number_history

        try:
            # Get new value for receiver
            value = getattr(host_obj, self.name)
        except UnsupportedAttributeError:
            return  # Not supported in current version.

        section: AoE2FileSection = sections[self.section_name]

        if self.is_special_unit_case:
            self._commit_special_unit_case(sections, value, scenario_version)
            return

        # Retrieve value without using eval() -- Eval is slow
        retriever = None
        file_section = section
        for index, item in enumerate(self.splitted_link):
            try:
                if "[" in item:
                    file_section = getattr(file_section, item[:-11])[number_hist[index]]
                else:
                    retriever = file_section.retriever_map[item]
            except KeyError as e:
                # Maybe not supported in current version. if actually not supported -> ignore
                if self.support is not None:
                    if not self.support.supports(scenario_version):
                        return
                raise e

        if retriever is None:
            raise ValueError("RetrieverObjectLink is unable to find retriever")

        if self.process_as_object:
            struct_datatype = retriever.datatype.var

            prefix = "struct:"
            if not struct_datatype.startswith(prefix):
                raise ValueError(
                    f"process_as_object isn't defined properly. Expected: '{prefix}...', got: '{struct_datatype}'"
                )

            struct_name = struct_datatype[len(prefix):]
            struct_model = file_section.struct_models[struct_name]

            RetrieverObjectLink.update_retriever_length(retriever, struct_model, len(value))
            RetrieverObjectLink.commit_object_list(value, sections, host_obj._instance_number_history, scenario_version)
        else:
            retriever.data = value

        if hasattr(retriever, 'on_commit'):
            handle_retriever_dependency(retriever, "commit", file_section, sections)

    @staticmethod
    def commit_object_list(object_list, sections, instance_number_history, scenario_version):
        obj: AoE2Object
        for index, obj in enumerate(object_list):
            obj._sections = sections
            obj._instance_number_history = instance_number_history + [index]
            obj.commit(scenario_version)

    @staticmethod
    def update_retriever_length(retriever, model, new_len):
        try:
            old_len = len(retriever.data)
        except TypeError:  # retriever.data was not set before (list of 0 -> None)
            old_len = 0
            retriever.data = []

        if new_len < old_len:
            retriever.data = retriever.data[:new_len]
        elif new_len > old_len:
            retriever.data += [AoE2FileSection.from_model(model, set_defaults=True) for _ in range(new_len - old_len)]

            if retriever.log_value:
                retriever._print_value_update(f"[{model.name}] * {old_len}", f"[{model.name}] * {new_len}")

    def _is_special_unit_case(self) -> bool:
        return ("[]" in self.link) if self.link else False

    def _construct_special_unit_case(self, sections, scenario_version):
        units = []
        value = sections[self.section_name]
        for index, item in enumerate(self.splitted_link):
            if "[]" in item:
                value = getattr(value, item[:-2])
            else:
                for player, player_units_section in enumerate(value):
                    player_units = getattr(player_units_section, item)
                    units.append(self.process_object_list(player_units, [player], sections, scenario_version))
        return units

    def _commit_special_unit_case(self, sections, value, scenario_version):
        for player, player_unit in enumerate(value):
            player_unit_retriever = sections["Units"].players_units[player]
            retriever_list = player_unit_retriever.retriever_map.values()
            units = player_unit_retriever.retriever_map["units"]
            # units = get_retriever_by_name(retriever_list, "units")
            struct_model = player_unit_retriever.struct_models["UnitStruct"]

            RetrieverObjectLink.update_retriever_length(units, struct_model, len(value[player]))
            RetrieverObjectLink.commit_object_list(player_unit, sections, [player], scenario_version)

            for retriever in retriever_list:
                if hasattr(retriever, 'on_commit'):
                    handle_retriever_dependency(retriever, "commit", player_unit_retriever, sections)

    def __repr__(self):
        return f"[RetrieverObjectLink] {self.name}: {self.section_name}.{self.link}" + \
               (f"\n\t- Process as: {self.process_as_object.__name__}" if self.process_as_object else "") + \
               (f"\n\t- Get Instance Number: True" if self.retrieve_instance_number else "") + \
               (f"\n\t- Get Hist Number: {self.retrieve_history_number}" if self.retrieve_history_number >= 0 else "")
