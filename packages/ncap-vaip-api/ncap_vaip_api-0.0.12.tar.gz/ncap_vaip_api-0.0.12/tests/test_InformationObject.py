import pytest
from vaip_api_class_mockup import InformationObject

class TestClass:
    def test_constructor(self):
        i_obj = InformationObject()
        print(i_obj)
        print("-=-" * 5)
        assert i_obj != None

    def test_add_structure_representation(self):
        i_obj = InformationObject()
        assert i_obj.hasStructureRepresentation == []
        assert str(type(i_obj.hasStructureRepresentation)) == "<class 'owlready2.prop.IndividualValueList'>"
        struct = i_obj.add_structure_representation("PrimaryLabel", "my value")
        assert i_obj.hasStructureRepresentation == [struct]

    def test_remove_structure_representation(self):
        i_obj = InformationObject()
        assert i_obj.hasStructureRepresentation == []
        struct = i_obj.add_structure_representation("PrimaryLabel2", "my value2")
        assert i_obj.hasStructureRepresentation == [struct]
        i_obj.remove_structure_representation(struct)
        assert i_obj.hasStructureRepresentation == []

    def test_add_semantic_representation(self):
        i_obj = InformationObject()
        assert i_obj.hasSemanticRepresentation == []
        assert str(type(i_obj.hasSemanticRepresentation)) == "<class 'owlready2.prop.IndividualValueList'>"
        struct = i_obj.add_semantic_representation("PrimaryLabel3", "my value3")
        assert i_obj.hasSemanticRepresentation == [struct]

    def test_remove_semantic_representation(self):
        i_obj = InformationObject()
        assert i_obj.hasSemanticRepresentation == []
        struct = i_obj.add_semantic_representation("PrimaryLabel4", "my value4")
        assert i_obj.hasSemanticRepresentation == [struct]
        i_obj.remove_semantic_representation(struct)
        assert i_obj.hasSemanticRepresentation == []

    def test_add_other_representation(self):
        i_obj = InformationObject()
        assert i_obj.hasOtherRepresentation == []
        assert str(type(i_obj.hasOtherRepresentation)) == "<class 'owlready2.prop.IndividualValueList'>"
        struct = i_obj.add_other_representation("PrimaryLabel5", "my value5")
        assert i_obj.hasOtherRepresentation == [struct]

    def test_remove_other_representation(self):
        i_obj = InformationObject()
        assert i_obj.hasOtherRepresentation == []
        struct = i_obj.add_other_representation("PrimaryLabel6", "my value6")
        assert i_obj.hasOtherRepresentation == [struct]
        i_obj.remove_other_representation(struct)
        assert i_obj.hasOtherRepresentation == []
