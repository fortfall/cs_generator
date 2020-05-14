cls_tmpl = r"""
using System.Collections.Generic;
{{#dynamic}}
using System.Dynamic;
{{/dynamic}}
using Newtonsoft.Json;

namespace {{namespace}}
{
    public partial class {{name}}    
    {
        {{#field}}
        public readonly {{fieldType}} {{fieldName}}; 
        {{/field}}

        [JsonConstructor]
        public {{name}}(
            {{#field}}
            {{paramType}} {{fieldName}}{{^endLine}},{{/endLine}}
            {{/field}}
        )
        {
            {{#field}}
            this.{{fieldName}} = {{fieldName}};
            {{/field}}
        }
    }
}
"""

enum_tmpl = r"""
using Newtonsoft.Json;

namespace {{namespace}}
{
    public enum {{name}}
    {
        {{#item}}
        {{itemName}} = {{itemValue}}{{^endLine}},{{/endLine}}
        {{/item}}
    }
}
"""