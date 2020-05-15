using System.Collections.Generic;
using Newtonsoft.Json;

namespace TestNamespace
{
    public partial class Person    
    {
        public readonly string name; 
        public readonly int age; 
        public readonly Job job; 
        public readonly IReadOnlyList<string> hobbies; 

        [JsonConstructor]
        public Person(
            string name,
            int age,
            Job job,
            List<string> hobbies
        )
        {
            this.name = name;
            this.age = age;
            this.job = job;
            this.hobbies = hobbies;
        }
    }
}
