### Considerations
* provide switch for whether ref keeping is required. if so, use IList/IDictionary, else use IReadOnlyList/IReadOnlyDictionary
* provide switch for whether to preserve class fields
  * if True, preserve all class fields for all classes
  * if False or empty dictionary/set, discard all class fields for all classes
  * non-empty dictionary/set, preserve those in the set, and those in the dictionary whose value is True
* difficulty: how to parse python type annotations into C# types