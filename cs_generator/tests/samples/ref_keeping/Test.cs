using System.Collections.Generic;
using System.Dynamic;
using Newtonsoft.Json;

namespace TestNamespace
{
    public partial class Test    
    {
        public readonly int int_var; 
        public readonly float float_var; 
        public readonly string str_var; 
        public readonly bool bool_var; 
        public readonly Job enum_var; 
        public readonly Dog cls_var; 
        public readonly int? nullable_int; 
        public readonly Job? nullable_enum; 
        public readonly Dog nullable_cls; 
        public readonly dynamic dynamic; 
        public readonly IList<float> lst_var; 
        public readonly IList<Dog> lst_nullable_dog; 
        public readonly IList<dynamic> lst_dynamic; 
        public readonly IList<int> tup_var; 
        public readonly IList<dynamic> tup_dynamic; 
        public readonly IDictionary<int, string> dct_int_str; 
        public readonly IDictionary<string, dynamic> dct_str_dynamic; 
        public readonly IDictionary<Job, float> dct_enum_float; 
        public readonly IList<IDictionary<string, Job?>> nested; 

        [JsonConstructor]
        public Test(
            int int_var,
            float float_var,
            string str_var,
            bool bool_var,
            Job enum_var,
            Dog cls_var,
            int? nullable_int,
            Job? nullable_enum,
            Dog nullable_cls,
            dynamic dynamic,
            List<float> lst_var,
            List<Dog> lst_nullable_dog,
            List<dynamic> lst_dynamic,
            List<int> tup_var,
            List<dynamic> tup_dynamic,
            Dictionary<int, string> dct_int_str,
            Dictionary<string, dynamic> dct_str_dynamic,
            Dictionary<Job, float> dct_enum_float,
            List<Dictionary<string, Job?>> nested
        )
        {
            this.int_var = int_var;
            this.float_var = float_var;
            this.str_var = str_var;
            this.bool_var = bool_var;
            this.enum_var = enum_var;
            this.cls_var = cls_var;
            this.nullable_int = nullable_int;
            this.nullable_enum = nullable_enum;
            this.nullable_cls = nullable_cls;
            this.dynamic = dynamic;
            this.lst_var = lst_var;
            this.lst_nullable_dog = lst_nullable_dog;
            this.lst_dynamic = lst_dynamic;
            this.tup_var = tup_var;
            this.tup_dynamic = tup_dynamic;
            this.dct_int_str = dct_int_str;
            this.dct_str_dynamic = dct_str_dynamic;
            this.dct_enum_float = dct_enum_float;
            this.nested = nested;
        }
    }
}
