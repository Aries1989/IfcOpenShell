import test.bootstrap
import ifcopenshell.api


class TestAppendAsset(test.bootstrap.IFC4):
    def test_do_not_append_twice(self):
        library = ifcopenshell.api.run("project.create_file")
        element = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWallType")
        material = ifcopenshell.api.run("material.add_material", library, name="Material")
        schedule = ifcopenshell.api.run("cost.add_cost_schedule", library, name="Schedule")
        profile = library.createIfcIShapeProfileDef()

        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=material)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=material)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=schedule)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=schedule)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=profile)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=profile)
        assert len(self.file.by_type("IfcWallType")) == 1

    def test_append_a_type_product(self):
        library = ifcopenshell.api.run("project.create_file")
        element = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWallType")
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element)
        assert len(self.file.by_type("IfcWallType")) == 1

    def test_append_a_type_product_with_its_materials(self):
        library = ifcopenshell.api.run("project.create_file")
        element = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWallType")
        material = ifcopenshell.api.run("material.add_material", library, name="Material")
        ifcopenshell.api.run("material.assign_material", library, product=element, material=material)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element)
        assert self.file.by_type("IfcWallType")[0].HasAssociations[0].RelatingMaterial.Name == "Material"

    def test_append_a_type_product_with_its_styles(self):
        library = ifcopenshell.api.run("project.create_file")
        element = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWallType")
        item = library.createIfcBoundingBox()
        library.createIfcStyledItem(Item=item)
        mapped_rep = library.createIfcShapeRepresentation(Items=[item])
        element.RepresentationMaps = [library.createIfcRepresentationMap(MappedRepresentation=mapped_rep)]
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element)
        assert self.file.by_type("IfcStyledItem")[0].Item == self.file.by_type("IfcBoundingBox")[0]

    def test_append_a_material(self):
        library = ifcopenshell.api.run("project.create_file")
        material = ifcopenshell.api.run("material.add_material", library, name="Material")
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=material)
        assert len(self.file.by_type("IfcMaterial")) == 1

    def test_append_a_cost_schedule(self):
        library = ifcopenshell.api.run("project.create_file")
        schedule = ifcopenshell.api.run("cost.add_cost_schedule", library, name="Schedule")
        item = ifcopenshell.api.run("cost.add_cost_item", library, cost_schedule=schedule)
        item2 = ifcopenshell.api.run("cost.add_cost_item", library, cost_item=item)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=schedule)
        assert len(self.file.by_type("IfcCostSchedule")) == 1
        assert len(self.file.by_type("IfcCostItem")) == 2
        assert self.file.by_type("IfcCostSchedule")[0].Name == "Schedule"
        appended_item = self.file.by_type("IfcCostSchedule")[0].Controls[0].RelatedObjects[0]
        assert appended_item.is_a("IfcCostItem")
        assert appended_item.IsNestedBy[0].RelatedObjects[0].is_a("IfcCostItem")

    def test_append_a_profile_def(self):
        library = ifcopenshell.api.run("project.create_file")
        profile = library.createIfcIShapeProfileDef()
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=profile)
        assert len(self.file.by_type("IfcIShapeProfileDef")) == 1

    def test_append_a_profile_def_with_all_properties(self):
        library = ifcopenshell.api.run("project.create_file")
        profile = library.createIfcIShapeProfileDef()
        ifcopenshell.api.run("pset.add_pset", library, product=profile, name="Foo_Bar")
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=profile)
        assert len(self.file.by_type("IfcIShapeProfileDef")) == 1
        assert self.file.by_type("IfcIShapeProfileDef")[0].HasProperties[0].Name == "Foo_Bar"

    def test_append_a_product(self):
        library = ifcopenshell.api.run("project.create_file")
        element = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWall")
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element)
        assert len(self.file.by_type("IfcWall")) == 1

    def test_append_a_product_with_all_properties(self):
        library = ifcopenshell.api.run("project.create_file")
        element = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWall")
        ifcopenshell.api.run("pset.add_pset", library, product=element, name="Foo_Bar")
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element)
        assert ifcopenshell.util.element.get_psets(self.file.by_type("IfcWall")[0])["Foo_Bar"]

    def test_append_a_product_with_its_type(self):
        library = ifcopenshell.api.run("project.create_file")
        element = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWall")
        element_type = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWallType")
        ifcopenshell.api.run("type.assign_type", library, related_object=element, relating_type=element_type)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element)
        assert ifcopenshell.util.element.get_type(self.file.by_type("IfcWall")[0]).is_a("IfcWallType")

    def test_append_only_specified_occurrences_of_a_typed_product(self):
        library = ifcopenshell.api.run("project.create_file")
        element = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWall")
        element2 = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWall")
        element3 = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWall")
        element_type = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWallType")
        ifcopenshell.api.run("type.assign_type", library, related_object=element, relating_type=element_type)
        ifcopenshell.api.run("type.assign_type", library, related_object=element2, relating_type=element_type)
        ifcopenshell.api.run("type.assign_type", library, related_object=element3, relating_type=element_type)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element2)
        assert len(ifcopenshell.util.element.get_types(self.file.by_type("IfcWallType")[0])) == 2
        assert len(self.file.by_type("IfcWall")) == 2

    def test_append_a_product_with_materials(self):
        library = ifcopenshell.api.run("project.create_file")
        element = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWall")
        material = ifcopenshell.api.run("material.add_material", library, name="Material")
        ifcopenshell.api.run("material.assign_material", library, product=element, material=material)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element)
        assert ifcopenshell.util.element.get_material(self.file.by_type("IfcWall")[0]).Name == "Material"

    def test_append_a_product_with_its_styles(self):
        library = ifcopenshell.api.run("project.create_file")
        element = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWall")
        item = library.createIfcBoundingBox()
        library.createIfcStyledItem(Item=item)
        representation = library.createIfcShapeRepresentation(Items=[item])
        element.Representation = library.createIfcProductDefinitionShape(Representations=[representation])
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element)
        assert self.file.by_type("IfcStyledItem")[0].Item == self.file.by_type("IfcBoundingBox")[0]

    def test_append_a_product_with_openings(self):
        library = ifcopenshell.api.run("project.create_file")
        element = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWall")
        opening = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcOpeningElement")
        ifcopenshell.api.run("void.add_opening", library, opening=opening, element=element)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element)
        assert self.file.by_type("IfcWall")[0].HasOpenings[0].RelatedOpeningElement.is_a("IfcOpeningElement")


class TestAppendAssetIFC2X3(test.bootstrap.IFC2X3):
    def test_append_a_product_with_its_type(self):
        library = ifcopenshell.api.run("project.create_file", version="IFC2X3")
        element = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWall")
        element_type = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWallType")
        ifcopenshell.api.run("type.assign_type", library, related_object=element, relating_type=element_type)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element)
        assert ifcopenshell.util.element.get_type(self.file.by_type("IfcWall")[0]).is_a("IfcWallType")

    def test_append_only_specified_occurrences_of_a_typed_product(self):
        library = ifcopenshell.api.run("project.create_file", version="IFC2X3")
        element = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWall")
        element2 = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWall")
        element3 = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWall")
        element_type = ifcopenshell.api.run("root.create_entity", library, ifc_class="IfcWallType")
        ifcopenshell.api.run("type.assign_type", library, related_object=element, relating_type=element_type)
        ifcopenshell.api.run("type.assign_type", library, related_object=element2, relating_type=element_type)
        ifcopenshell.api.run("type.assign_type", library, related_object=element3, relating_type=element_type)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element)
        ifcopenshell.api.run("project.append_asset", self.file, library=library, element=element2)
        assert len(ifcopenshell.util.element.get_types(self.file.by_type("IfcWallType")[0])) == 2
        assert len(self.file.by_type("IfcWall")) == 2
