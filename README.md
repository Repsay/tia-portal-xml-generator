# tia-xml-generator

tia-xml-generator is a Python library created for generating XML files that can be imported into TIA Portal via TIA Openness. The library was created as part of a graduation project and currently supports the creation of DB, FB, and OB blocks.

## Usage

Here's an example of how to use tia-xml-generator to create a DB block:

```python
from tia_xml_generator.elements import document
from tia_xml_generator.enums import MemoryLayout

doc = document.Document()
db = doc.add_db("__NAME__")
db.add_static("__NAME__", "__TYPE__")
db.author = "__Author__"
db.family = "__Family__"
db.version = "1.0"
db.memory_layout = MemoryLayout.Standard.name
doc.save_template("__TEMPLATE_NAME__", True) # Gives PKL file
doc.save("__OUTPUT_NAME__") # Gives XML file
```

The code above creates a new instance of the Document class from tia_xml_generator.elements, adds a DB block to it, sets some properties of the block, saves the block as a pkl file using the save_template method, and saves the entire document as an XML file using the save method.

## Contributing

If you'd like to contribute to tia-xml-generator, please fork the repository and create a new branch for your changes. Once you've made your changes, submit a pull request and we'll review your changes.

## License

tia-xml-generator is licensed under the MIT license. See the LICENSE file for more information.
