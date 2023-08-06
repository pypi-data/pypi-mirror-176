from vaip_api_class_mockup import vaip, VaipUtils

granule = vaip._create_aiu("Granule")

file_content = granule.add_content("File", "{{runtime_placeholder}}")
file_content.add_semantic_representation("File Schema", "{{placholder}}")
file_content.add_structure_representation("File Format", "{{placeholder}}")
file_content.add_other_representation("Decoding Software", "{{placeholder}}")
file_content.add_other_representation("Visualization Software", "{{placeholder}}")

desc = granule.add_description("Product Description", "{{placeholder}}")
desc.add_semantic_representation("Foo", "bar")
desc.add_structure_representation("Foo", "bar")

packaging = granule.add_packaging("Packaging", "{{placeholder}}")
packaging.add_semantic_representation("Packaging Strategy", "{{placeholder}}")
packaging.add_structure_representation("Packaging Format", "{{placeholder}}")

checksum = granule.add_fixity("Checksum", "{{runtime_placeholder}}")
checksum.add_semantic_representation("Checksum Definition", "https://en.wikipedia.org/wiki/Checksum")
checksum.add_structure_representation("Checksum Format", "{{runtime_placeholder}}")
checksum.add_other_representation("Checksum Purpose", "This checksum is created at the archival time and is served with the data to verify the integrity of the file downloaded by a consumer.")

ar1 = granule.add_access_rights("Distribution License", "Distribution liability: NOAA and NCEI make no warranty, expressed or implied, regarding these data, nor does the fact of distribution constitute such a warranty. NOAA and NCEI cannot assume liability for any damages caused by any errors or omissions in these data. If appropriate, NCEI can only certify that the data it distributes are an authentic copy of the records that were accepted for inclusion in the NCEI archives.")
ar1.add_semantic_representation("Foo", "bar")
ar1.add_structure_representation("Foo", "bar")

ar2 = granule.add_access_rights("Use License", "Use liability: NOAA and NCEI cannot provide any warranty as to the accuracy, reliability, or completeness of furnished data. Users assume responsibility to determine the usability of these data. The user is responsible for the results of any application of this data for other than its intended purpose.")
ar2.add_semantic_representation("Foo", "bar")
ar2.add_structure_representation("Foo", "bar")

ctx = granule.add_context("Provider", "{{placeholder}}")
ctx.add_semantic_representation("Foo", "bar")
ctx.add_structure_representation("Foo", "bar")

prov = granule.add_provenance("Producing Software", "{{placeholder}}")
prov.add_semantic_representation("Foo", "bar")
prov.add_structure_representation("Foo", "bar")

ref1 = granule.add_reference("Provider PID", "{{runtime_placeholder}}")
ref1.add_semantic_representation("Foo", "bar")
ref1.add_structure_representation("Foo", "bar")

ref2 = granule.add_reference("Archive PID", "{{runtime_placeholder}}")
ref2.add_semantic_representation("Foo", "bar")
ref2.add_structure_representation("Foo", "bar")

r = granule.validate()

print(granule.serialize_rdf_text("nt"))
# VaipUtils.visualize_pattern(granule)