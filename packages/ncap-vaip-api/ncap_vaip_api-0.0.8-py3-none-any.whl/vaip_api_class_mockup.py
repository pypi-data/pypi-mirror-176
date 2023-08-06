#Using owlready2 to load the core ontology in-memory and then automatically generate Python classes for constructing RDF triples
from owlready2 import get_ontology, default_world, Thing, World # type: ignore  # pylint: disable=E0401
#Suggest looking at uuid to do uuid generation for graph IRIs.
import uuid  # pylint: disable=E0401
from pyshacl import validate
import hashlib


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
    def _create_aiu(primary_label, supporting_labels=None):
        aiu = ArchivalInformationUnit(VaipUtils.generate_uuid_str(), namespace=entity)
        vaip.set_labels(aiu, primary_label, supporting_labels)
        return aiu

    def set_labels(node, primary, supporting):
        node.prefLabel = primary
        node.label.append(primary)
        if supporting is not None:
            node.label.extend(supporting)

### The following class represents and groups behaviors that will be generally useful to library objects and structures.###


class VaipUtils:
    """vAIP Utils is a static class container to group typical vaip utilities that are used by the system.
    Note that python doesn't really need static utility classes and these methods should really be in a standalone module, they are included this way for development purposes so
    we can attach this docstring to them.
    """

    def generate_uuid_str(seed: str = None) -> str:
        """Generates a globally unique uuid, typically used in creating a unique IRI for a node to be stored in the knowledge graph.
        """
        if seed is not None:
            md5 = hashlib.md5()
            md5.update(seed.encode('utf-8'))

            return str(uuid.UUID(hex=md5.hexdigest(), version=4))
        else:
            return str(uuid.uuid4())

    def generate_iri(namespace: str, root="https://doc.noaa.nesdis.ncei.gov/noaa_knowledge_graph") -> str:
        """Generates a unique IRI for a node to be stored in the knowledge graph.
        The 'namespace' string is notionally context dependent and hierarchically constructed:
            - In the case of creating new graph pattern resources, 
             - IRIs of data objects should terminate as UUID prefixed by parent information object's IRI
             - IRIs of information objects should terminate as UUID prefixed by parent information package IRI
             - IRIs of information packages should terminate as UUID prefixed by "{{root}}/patterns/{{class}}/" (where class==AIU,AIC,DIP)
            - In the case of creating new template record resources,
             - IRIs of storage template (AIU,AIC, or DIP) root nodes should follow "{{root}}/templates/{{class}}/{{pattern}}/{{template}}"
            - In the case of creating new graph record resources,
             - IRIs of storage record root nodes (AIU, AIC, or DIP) should follow "{{root}}/records/{{class}}/{{pattern}}/{{template}}/{{record}}"
        Args:
            uuid (_type_, optional): _description_. Defaults to uuid.
        """
        return f"{root}/{namespace}/{VaipUtils.generate_uuid_str()}"

    def generate_placeholder_variable(placeholder_label=None):
        """Generates a placeholder value for the 'hasBits' target for an IRI. Placeholder value may be randomly generated with qualifying namespace in value
        if needed, but please note doing placeholder matching will rely on contextualized key (not the value itself).
        """
        return f"{placeholder_label}_{VaipUtils.generate_uuid_str()}"

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

        rdf_graph = pattern.as_rdflib_graph()
        nx_graph = rdflib_to_networkx_multidigraph(rdf_graph)
        pos = nx.spring_layout(nx_graph, iterations=200, scale=2)
        edge_labels = nx.get_edge_attributes(nx_graph, 'r')
        nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels)
        nx.draw(nx_graph, pos=pos)
        plt.show()

onto = get_ontology("file://./data/vaip-0.3.2-ontology.owl").load()
entity = onto.get_namespace("https://ncei.noaa.gov/ontologies/vaip/core/0.3.2/entities/")
skos = get_ontology("http://www.w3.org/2004/02/skos/core#").load() # skos:prefLabel is used for primary labeling of all nodes

###The following classes define most of the concepts in the vAIP along with methods that are relevant to each.###


### THE INFORMATION OBJECT SET ###

class InformationObject(Thing):
    """InformationObject is the fundamental data structure of the vAIP Knowledge graph and is taken directly from the OAIS reference model and encoded in RDF in the knowledge graph.
    Users do not create InformationObjects directly, but use specialized subclasses (Content, StructureRepresentation, SemanticRepresentation, Description, Packaging, etc.). Creating an information object
    to user methods looks like choosing an appropriate sublcass of InformationObject and providing a primary label, optional supporting labels, deciding on the type of data being held (linked or valued), and
    adding 
        adding 
    adding 
    """
    namespace = onto

    def as_rdflib_graph(self):
        graph = default_world.as_rdflib_graph()
        return graph

    def serialize_rdf_text(self, format="xml"):
        """Converts the owlready2 active ontology into an rdflib graph, and then calls rdflib.Graph.serialize to return a string
        """
        graph = default_world.as_rdflib_graph()
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
        data = onto.DigitalObject(VaipUtils.generate_uuid_str(), namespace=entity, hasBits=[link])
        vaip.set_labels(data, f"{primary_label} Link", supporting_labels)
        self.hasDataObject.append(data)
        return data

    def set_valued_data(self, primary_label: str, value: str, supporting_labels=None):
        data = onto.DigitalObject(VaipUtils.generate_uuid_str(), namespace=entity, hasBits=[value])
        vaip.set_labels(data, f"{primary_label} Value", supporting_labels)
        self.hasDataObject.append(data)
        return data

    def add_structure_representation(self, primary_label: str, value: str, supporting_labels=None):
        node = onto.StructureRepresentation(VaipUtils.generate_uuid_str(), namespace=entity)
        vaip.set_labels(node, primary_label, supporting_labels)
        self.hasStructureRepresentation.append(node)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        return node

    def remove_structure_representation(self, structure_representation):
        while structure_representation in self.hasStructureRepresentation:
            self.hasStructureRepresentation.remove(structure_representation)

    def add_semantic_representation(self, primary_label: str, value: str, supporting_labels=None):
        node = onto.SemanticRepresentation(VaipUtils.generate_uuid_str(), namespace=entity)
        vaip.set_labels(node, primary_label, supporting_labels)
        self.hasSemanticRepresentation.append(node)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        return node

    def remove_semantic_representation(self, semantic_representation):
        while semantic_representation in self.hasSemanticRepresentation:
            self.hasSemanticRepresentation.remove(semantic_representation)

    def add_other_representation(self, primary_label: str, value: str, supporting_labels=None):
        node = onto.OtherRepresentation(VaipUtils.generate_uuid_str(), namespace=entity)
        vaip.set_labels(node, primary_label, supporting_labels)
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
    namespace = onto

    def validate(self):
        """Intentionally left empty for implementation by inheriting classes
        """
        pass
    
    def as_rdflib_graph(self):
        graph = default_world.as_rdflib_graph()
        return graph
    
    def serialize_rdf_text(self, format="xml"):
        graph = default_world.as_rdflib_graph()
        return graph.serialize(destination=None, format=format, encoding="utf-8").decode("utf-8")

    def add_description(self, primary_label: str, value: str, supporting_labels=None):
        node = onto.UnitDescription(VaipUtils.generate_uuid_str(), namespace=entity)
        vaip.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)

        self.describedBy.append(node)
        node.derivedFromPackage.append(self)

        return node

    def add_content(self, primary_label: str, value: str, supporting_labels=None):
        node = onto.ContentInformationObject(VaipUtils.generate_uuid_str(), namespace=entity)
        vaip.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)

        self.hasContentInformation.append(node)

        return node

    def add_packaging(self, primary_label: str, value: str, supporting_labels=None):
        node = onto.PackagingInformationObject(VaipUtils.generate_uuid_str(), namespace=entity)
        vaip.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.packagedBy.append(node)

        return node

    def add_fixity(self, primary_label: str, value: str, supporting_labels=None):
        node = onto.FixityPreservation(VaipUtils.generate_uuid_str(), namespace=entity)
        vaip.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.hasFixity.append(node)

        return node

    def add_access_rights(self, primary_label: str, value: str, supporting_labels=None):
        node = onto.AccessRightsPreservation(VaipUtils.generate_uuid_str(), namespace=entity)
        vaip.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.hasAccessRights.append(node)

        return node
    
    def add_context(self, primary_label: str, value: str, supporting_labels=None):
        node = onto.ContextPreservation(VaipUtils.generate_uuid_str(), namespace=entity)
        vaip.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.hasContext.append(node)

        return node
    
    def add_provenance(self, primary_label: str, value: str, supporting_labels=None):
        node = onto.ProvenancePreservation(VaipUtils.generate_uuid_str(), namespace=entity)
        vaip.set_labels(node, primary_label, supporting_labels)
        node.set_valued_data(primary_label, value, supporting_labels=supporting_labels)
        
        self.hasProvenance.append(node)

        return node

    def add_reference(self, primary_label: str, value: str, supporting_labels=None):
        node = onto.ReferencePreservation(VaipUtils.generate_uuid_str(), namespace=entity)
        vaip.set_labels(node, primary_label, supporting_labels)
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
    namespace = onto
    
    def validate(self):
        graph = self.as_rdflib_graph()
        r = validate(graph, shacl_graph="./data/shacl/vaip_aiu.shacl")
        conforms, results_graph, results_text = r
        print(results_text)
        return {
            "conforms": conforms,
            "results_graph": results_graph,
            "results_text": results_text
        }


    class ArchivalInformationCollection(Thing):
        namespace = onto
        pass


    class DisseminationInformationPackage(Thing):
        namespace = onto
        pass
