#Using owlready2 to load the core ontology in-memory and then automatically generate Python classes for constructing RDF triples
from owlready2 import get_ontology, Thing, World # type: ignore  # pylint: disable=E0401
#Suggest looking at uuid to do uuid generation for graph IRIs.
import uuid  # pylint: disable=E0401
from pyshacl import validate
import hashlib
import os
import io


### The following class represents behaviors that will be user exposed and leverage the internal package classes and libraries###
class VaipOnto:

    def __init__(self, uri):
        # body of the constructor
        self.onto = get_ontology(uri).load()
        self.namespace = self.onto.get_namespace("https://ncei.noaa.gov/ontologies/vaip/core/0.3.2/entities/")
        self.skos = get_ontology("http://www.w3.org/2004/02/skos/core#").load() # skos:prefLabel is used for primary labeling of all nodes


### The following class represents behaviors that will be user exposed and leverage the internal package classes and libraries###
class vaip:
    """There should be a top level namespace or namespace hierarchy that abstracts and exposes most of the behaviors of this library for use in a REST API.
    Examples of this are 'vaip.create_aiu_pattern()'. Alternatively, vaip.patterns.create_aiu_pattern().
    """

### The following class represents and groups behaviors that will be generally useful to library objects and structures.###


class VaipUtils:
    """vAIP Utils is a static class container to group typical vaip utilities that are used by the system.
    Note that python doesn't really need static utility classes and these methods should really be in a standalone module, they are included this way for development purposes so
    we can attach this docstring to them.
    """

    #TODO: Harden method, prettify method, return message in case nothing defined, allow help on class or object (method overloading)
    @staticmethod
    def get_definition(concept):
    #Return proper content on user asking about things they are creating/have created
        try:
            return concept.definition[0]
        except:
            return type(concept).definition[0]

    #TODO: Harden method, prettify method, return message in case nothing defined, allow help on class or object (method overloading)
    @staticmethod
    def get_example(concept):
        try:
            return concept.example[0]
        except:
            return type(concept).example[0]

    @staticmethod
    def get_file_resource_path(file_name, root_dir=os.path.dirname(__file__), prefix="", stem_dir="data"):
        resource_dir = f"{root_dir}/{stem_dir}"
        fully_qualified_path = f"{prefix}{resource_dir}/{file_name}"
        return fully_qualified_path

    @staticmethod
    def generate_node_id(seed: str = None):
        """Generates a globally unique uuid, typically used in creating a unique IRI for a node to be stored in the knowledge graph.
        """
        if seed is not None:
            md5 = hashlib.md5()
            md5.update(seed.encode('utf-8'))
            return str(uuid.UUID(hex=md5.hexdigest(), version=4))
        else:
            return str(uuid.uuid4())
    
    @staticmethod
    def get_root_namespace():
        return "https://ncei.noaa.gov/vaip"

    @staticmethod
    def get_pattern_namespace():
        return f"{VaipUtils.get_root_namespace()}/pattern"

    @staticmethod
    def get_storage_pattern_namespace():
        return f"{VaipUtils.get_pattern_namespace()}/storage"

    @staticmethod
    def get_aiu_pattern_namespace():
        return f"{VaipUtils.get_storage_pattern_namespace()}/aiu"

    @staticmethod
    def get_individual_aiu_pattern_namespace(pattern_id: str):
        return f"{VaipUtils.get_aiu_namespace()}/{pattern_id}"

    @staticmethod
    def get_dynamic_namespace(pattern):
        return pattern.namespace.ontology.get_namespace(f"{pattern.iri}/")
    
    @staticmethod
    def get_ontology_file_string(onto_file: str ="vaip_core_model.owl"):
        return VaipUtils.get_file_resource_path(onto_file, prefix="file://")
    
    @staticmethod
    def set_labels(node, primary, supporting):
        node.prefLabel = primary
        if supporting is not None:
            node.altLabel.extend(supporting)
        
    @staticmethod
    def load_core_shacl(shapes_file_name="vaip_core_shapes.shacl"):
        """
        Returns the core shacl file for vaip shapes into memory (currently just aiu pattern).
        """
        shapes_file_path = VaipUtils.get_file_resource_path(shapes_file_name, prefix="file://", stem_dir="data/shacl")
        if os.path.isfile(shapes_file_path):
            shapes_file = open(shapes_file_path, "r")
            shapes_string = shapes_file.read()
            shapes_file.close()
            return shapes_string
        else:
            return None

    def visualize_pattern(pattern, classes=False, values=True, supporting_labels=False):
        """Produces a visualization of a specific pattern

        Args:
            pattern (InformationObject or InformationPackage, required) Specifies the resource to visualize, takes a triples graph and produces a visualization for printing.
            classes (bool, optional): Displays classes alongside the pattern instances. Defaults to False.
            values (bool, optional): Displays data values (hasBits edges and values) alongside the pattern. Defaults to True.
            supporting_labels (bool, optional): Displays all supporting label triples for all nodes in the pattern. If False, only the primary label is shown. Defaults to False.
        """
        from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
        import networkx as nx
        import matplotlib.pyplot as plt
        import kglab
        import pyvis.network as pvn

        rdf_text = pattern.serialize_rdf_text("ttl")
        kg = kglab.KnowledgeGraph()
        kg.load_rdf_text(rdf_text)

        # measure = kglab.Measure()
        # measure.measure_graph(kg)

        # print("edges: {}\n".format(measure.get_edge_count()))
        # print("nodes: {}\n".format(measure.get_node_count()))

        pyvis_graph = pvn.Network(notebook=True)

        pyvis_graph.add_node(0, label="foo", title="This is FOO", color="red", size=9)
        pyvis_graph.add_node(1, label="bar", title="That is BAR", color="blue", size=5)
        pyvis_graph.add_node(2, label="baz", title="Here is BAZ", color="green", size=3)

        pyvis_graph.add_edge(0, 1, label="xyzzy", color="gray")
        pyvis_graph.add_edge(0, 2, label="fubar", color="red")

        pyvis_graph.force_atlas_2based()
        pyvis_graph.show("tmp.fig02.html")

        VIS_STYLE = {
            "wtm": {
                "color": "orange",
                "size": 40,
            },
            "ind":{
                "color": "yellow",
                "size": 30,
            },
        }

        subgraph = kglab.SubgraphTensor(kg)
        pyvis_graph = subgraph.build_pyvis_graph(style=VIS_STYLE)
        pyvis_graph.force_atlas_2based()
        # pyvis_graph.show_buttons(filter_=['physics'])
        # pyvis_graph.set_options('"bgcolor": "#222222"')
        pyvis_graph.show("tmp.fig01.html")

        # pos = nx.spring_layout(nx_graph, iterations=200, scale=2)
        # edge_labels = nx.get_edge_attributes(nx_graph, 'r')
        # nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels)
        # nx.draw(nx_graph, pos=pos)
        # plt.show()

def load_pattern_ontology(world=World(), ontology_root="https://ncei.noaa.gov/vaip/patterns/", ontology_stem=""):
    """
    Given an ontology root and an ontology stem, open a clean ontology in the specified world as the specified path.
    Do not enforce a join character for the two ontology strings, allow for use of # or / (or other) delimiters.
    ontology_path = f"{ontology_root}{ontology_stem}"
    pattern_ontology = world.get_ontology(ontology_path)
    return pattern_ontology
    """
    return world.get_ontology(f"{ontology_root}{ontology_stem}")

vaip_ontology = get_ontology(VaipUtils.get_ontology_file_string()).load()
aiu_ontology = load_pattern_ontology(vaip_ontology.world, VaipUtils.get_aiu_pattern_namespace())
skos = get_ontology("http://www.w3.org/2004/02/skos/core#").load() # skos:prefLabel is used for primary labeling of all nodes

###The following classes define most of the concepts in the vAIP along with methods that are relevant to each.###


### THE INFORMATION OBJECT SET ###



def create_aiu_pattern(primary_label, supporting_labels=None):
    aiu = ArchivalInformationUnit(VaipUtils.generate_node_id(), namespace=aiu_ontology.get_namespace(f'{VaipUtils.get_aiu_pattern_namespace()}/'))
    VaipUtils.set_labels(aiu, primary_label, supporting_labels)
    return aiu

class InformationObject(Thing):
    """InformationObject is the fundamental data structure of the vAIP Knowledge graph and is taken directly from the OAIS reference model and encoded in RDF in the knowledge graph.
    Users do not create InformationObjects directly, but use specialized subclasses (Content, StructureRepresentation, SemanticRepresentation, Description, Packaging, etc.). Creating an information object
    to user methods looks like choosing an appropriate sublcass of InformationObject and providing a primary label, optional supporting labels, deciding on the type of data being held (linked or valued), and
    adding 
        adding 
    adding 
    """
    namespace = vaip_ontology

    def as_rdflib_graph(self):
        graph = self.namespace.ontology.world.as_rdflib_graph()
        return graph

    def serialize_rdf_text(self, format="xml"):
        """Converts the owlready2 active ontology into an rdflib graph, and then calls rdflib.Graph.serialize to return a string
        """
        graph = self.namespace.ontology.world.as_rdflib_graph()
        return graph.serialize(destination=None, format=format, encoding="utf-8").decode("utf-8")

    def set_linked_data(self, primary_label: str, link: str, supporting_labels=None):
        """Set linked data in this InformationObject.

        Args:
            primary_label (str): Name of the linked data
            link (str): URL of data
            supporting_labels (str, optional): Additional labels for the linked data. Defaults to None.

        Returns:
            DigitalObject: the linked data object
        """
        data = vaip_ontology.DigitalObject(VaipUtils.generate_node_id(), namespace=VaipUtils.get_dynamic_namespace(self), hasBits=[link])
        VaipUtils.set_labels(data, f"{primary_label} Link", supporting_labels)
        self.hasDataObject.append(data)
        return data

    def set_valued_data(self, primary_label: str, value: str, supporting_labels=None):
        data = vaip_ontology.DigitalObject(VaipUtils.generate_node_id(), namespace=VaipUtils.get_dynamic_namespace(self), hasBits=[value])
        VaipUtils.set_labels(data, f"{primary_label} Value", supporting_labels)
        self.hasDataObject.append(data)
        return data

    def add_structure_representation(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.StructureRepresentation(VaipUtils.generate_node_id(), namespace=VaipUtils.get_dynamic_namespace(self))
        VaipUtils.set_labels(node, primary_label, supporting_labels)
        self.hasStructureRepresentation.append(node)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        return node

    def remove_structure_representation(self, structure_representation):
        while structure_representation in self.hasStructureRepresentation:
            self.hasStructureRepresentation.remove(structure_representation)

    def add_semantic_representation(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.SemanticRepresentation(VaipUtils.generate_node_id(), namespace=VaipUtils.get_dynamic_namespace(self))
        VaipUtils.set_labels(node, primary_label, supporting_labels)
        self.hasSemanticRepresentation.append(node)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        return node

    def remove_semantic_representation(self, semantic_representation):
        while semantic_representation in self.hasSemanticRepresentation:
            self.hasSemanticRepresentation.remove(semantic_representation)

    def add_other_representation(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.OtherRepresentation(VaipUtils.generate_node_id(), namespace=VaipUtils.get_dynamic_namespace(self))
        VaipUtils.set_labels(node, primary_label, supporting_labels)
        self.hasOtherRepresentation.append(node)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        return node

    def remove_other_representation(self, other_representation):
        while other_representation in self.hasOtherRepresentation:
            self.hasOtherRepresentation.remove(other_representation)

### THE INFORMATION PACKAGE SET ###

class InformationPackage(Thing):
    """Base class that isn't used directly. It should be used through one of its subclasses. 
    InformationPackages represent patternable storage in the knowledge graph.
    All resources in the knowledge graph are representable as whole InformationPackages.
    """
    namespace = vaip_ontology

    def validate(self):
        """Intentionally left empty for implementation by inheriting classes
        """
        pass
    
    def as_rdflib_graph(self):
        graph = self.namespace.ontology.world.as_rdflib_graph()
        return graph
    
    def serialize_rdf_text(self, serialization_format="rdfxml", return_as_string=True, qualified_save_path=f'{VaipUtils.get_file_resource_path(f"serialized_graph.owl")}'):
        if return_as_string:
            graph_file = io.BytesIO()
        else:
            graph_file = VaipUtils.get_file_resource_path(qualified_save_path)
        self.namespace.ontology.save(file = graph_file, format = serialization_format)
        if return_as_string:
            rdf_string = (graph_file.getvalue().decode("utf-8"))
            graph_file.close()
            return rdf_string
        return None

    def add_description(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.UnitDescription(VaipUtils.generate_node_id(), namespace=VaipUtils.get_dynamic_namespace(self))
        VaipUtils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)

        self.describedBy.append(node)
        node.derivedFromPackage.append(self)

        return node

    def add_content(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.ContentInformationObject(VaipUtils.generate_node_id(), namespace=VaipUtils.get_dynamic_namespace(self))
        VaipUtils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)

        self.hasContentInformation.append(node)

        return node

    def add_packaging(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.PackagingInformationObject(VaipUtils.generate_node_id(), namespace=VaipUtils.get_dynamic_namespace(self))
        VaipUtils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.packagedBy.append(node)

        return node

    def add_fixity(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.FixityPreservation(VaipUtils.generate_node_id(), namespace=VaipUtils.get_dynamic_namespace(self))
        VaipUtils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.hasFixity.append(node)

        return node

    def add_access_rights(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.AccessRightsPreservation(VaipUtils.generate_node_id(), namespace=VaipUtils.get_dynamic_namespace(self))
        VaipUtils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.hasAccessRights.append(node)

        return node
    
    def add_context(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.ContextPreservation(VaipUtils.generate_node_id(), namespace=VaipUtils.get_dynamic_namespace(self))
        VaipUtils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.hasContext.append(node)

        return node
    
    def add_provenance(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.ProvenancePreservation(VaipUtils.generate_node_id(), namespace=VaipUtils.get_dynamic_namespace(self))
        VaipUtils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.hasProvenance.append(node)

        return node

    def add_reference(self, primary_label: str, value: str, supporting_labels=None):
        node = vaip_ontology.ReferencePreservation(VaipUtils.generate_node_id(), namespace=VaipUtils.get_dynamic_namespace(self))
        VaipUtils.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.hasReference.append(node)

        return node

class ArchivalInformationUnit(Thing):
    """Archive Information Units relate to patterning and recording of identity of any type of entity that might be stored in the knowledge graph.
    This includes things like users, roles, orders, granules, collection records, files, cruises, models, code packages, etc.
    ArchivalInformationUnits should be stored as the data object for AIU pattern metadata. Creating an AIU pattern means creating and persisting a new pattern metadata
    record that holds a new central AIU node of an information package. All information objects are related to information packages through relationship to the central node.
    The central node of the ArchivalInformationUnit is considered the IRI of the entire 'pattern' or thing and other things are logically stored in relationship to it.
    """
    namespace = vaip_ontology
    
    def validate(self):
        graph = self.as_rdflib_graph()
        r = validate(graph, shacl_graph=VaipUtils.load_core_shacl())
        conforms, results_graph, results_text = r
        print(results_text)
        return {
            "conforms": conforms,
            "results_graph": results_graph,
            "results_text": results_text
        }
