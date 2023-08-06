from python_prtg import writers


def test_write(xml_writer: writers.XmlWriter, json_writer: writers.JsonWriter) -> None:
    assert isinstance(xml_writer, writers.XmlWriter)
    assert isinstance(json_writer, writers.JsonWriter)
    xml_writer.write()
    json_writer.write()
    assert xml_writer.filename == json_writer.filename
