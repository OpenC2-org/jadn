# JADN

JSON Abstract Data Notation (JADN) is a language-neutral, platform-neutral,
and format-neutral mechanism for serializing structured data.
JADN data structures are defined using the JSON document format described here.

An example data structure is shown below in various formats.  This example,
from the Protocol Buffers documentation, defines a message containing
information about a person:

    message Person {
        required string name = 1;
        required int32 id = 2;
        optional string email = 3;
    }

The Thrift equivalent is:

    struct Person {
        1: string name,
        2: i32 id,
        3: optional string email
    }

And the JADN version is:

    {   "meta": {
            "module": "protobuf-example1"},
        "types": [
            ["Person", "Record", [], "", [
                [1, "name", "String", [], ""],
                [2, "id", "Integer", [], ""],
                [3, "email", "String", ["[0"], ""]]
    ]]}

Although JADN can be edited directly, it is also possible to document
data structures using an interface definition language (IDL) such as
Thrift [1] or Protobuf [2], and translate the definitions into JADN format.
The advantage of JADN is that an IDL parser is not needed in order to use it.
JADN is designed for machine consumption and is read using the standard
JSON loader present in most programming languages.

A JADN file contains a list of datatype definitions in a fixed
format.  As shown in the example, each type definition is a list containing
four elements, plus for structured types, a list of field definitions.

### Type definitions
A type definition consists of:
 * name of the type being defined
 * base type from the set of built-in JADN types
 * type options
 * type description
 * field definitions if base type is a structure type

### Field definitions
If the base type is Enumerated, each field definition is a list of
three elements:
 * tag assigned to the item
 * name of the item
 * item description

If the base type is another structure type (Array, Choice, Map, Record),
each field definition is a list of five items:
 * tag or ordinal position of the field
 * name of the field
 * type of the field (built-in or user-defined)
 * field options
 * field description

## Built-in Data Types

A JADN syntax is defined using the following data types:

### Primitive Types

|   Type   | Description |
|---------:|-------------|
Binary     | A sequence of octets or bytes. Serialized either as binary data or as a string using an encoding such as hex or base64.
Boolean    | A logical entity that can have two values: true, and false.  Serialized as either integer or keyword.
Integer    | A number that can be written without a fractional component.  Serialized either as binary data or a text string.
Number     | A real number.  Valid values include integers, rational numbers, and irrational numbers.  Serialized as either binary data or a text string.
Null       | Nothing, used to designate fields with no value.  Serialized as an empty string.
String     | A sequence of characters.  Each character must have a valid Unicode codepoint.

### Structure Types

|   Type   | Description |
|---------:|-------------|
Array      | An ordered list of unnamed fields.  Each field has an ordinal position and a type.  Serialized as a list.
ArraryOf   | An ordered list of unnamed fields of the same type.  Each field has an ordinal position and must be the specified type.  Serialized as a list.
Choice     | One field selected from a set of named fields.  The value has a name and a type. Serialized as a one-element map.
Enumerated | A set of id:name pairs.  Serialized as either the integer id or the name string.
Map        | An unordered set of named fields.  Each field has a name and a type.  Serialized as a mapping type (referred to in various programming languages as: associative array, dict, dictionary, hash, map, object).
Record     | An ordered list of named fields, e.g. a message, record, structure, or row in a table.  Each field has an ordinal position, a name, and a type. Serialized as either a list or a map.

## Option Tags/Keys

The JADN Type Options (TOPTS) and Field Options (FOPTS) elements are a list of strings where each string is an option.
The first character is the type ID; the remaining characters are the value.
The option string is converted into a Name: Value pair before use, where the Name corresponds to the type ID
and the Value has the type shown in the tables.

### Type Options

|  ID  | Name    | ID Char | Type | Description |
|------|---------|:---:|---------|--------------|
  0x3d | etag    |  =  | boolean | enumerated type is serialized as tag, default=false, field name is ignored if present)
  0x5b | min     |  [  | integer | minimum string length, integer value, array length, or property count
  0x5d | max     |  ]  | integer | maximum string length, integer value, array length, or property count
  0x23 | aetype  |  #  | string  | ArrayOf element type
  0x24 | pattern |  $  | string  | regular expression that a string type must match
  0x40 | format  |  @  | string  | name of validation function, e.g., date-time, email, ipaddr, ...

### Field Options
|  ID  | Name    | ID Char | Type | Description |
|------|---------|:---:|---------|--------------|
  0x5b | min     |  [  | integer | minimum cardinality of field, default = 1, 0 = field is optional
  0x5d | max     |  ]  | integer | maximum cardinality of field, default = 1, 0 = inherited max. If max != 1, field is an array.
  0x26 | atfield |  &  | string  | name of a field that specifies the type of this field
  0x2f | etype   |  /  | string  | serializer-specific encoding type, e.g., u8, i32, hex, base64
  0x21 | default |  !  | string  | default value for this field (coerced to field type)

## Serialization
Thrift and Protobuf each define a specific format for serialized data.  JADN is format-independent,
which allows messages to be serialized using a format most suited to the application.

An instance of a JADN structure called Test1 consisting of a single integer named "a" with the value 150:

    ["Test1", "Record", [], "", [
        [1, "a", "Integer", [], ""]]
    ]

would be serialized in Protobuf format [3] as three hex bytes:

    08 96 01

The same instance would be serialized in JSON format as the nine byte string:

    {"a":150}

or in minified JSON format as the five byte string:

    [150]

A codec (encoder/decoder) serializes and de-serializes JADN message instances using the
selected serialization format.

## References

[1] https://thrift.apache.org/docs/idl

[2] https://developers.google.com/protocol-buffers/

[3] https://developers.google.com/protocol-buffers/docs/encoding