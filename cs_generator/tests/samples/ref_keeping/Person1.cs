
using System.Collections.Generic;
using Newtonsoft.Json;

namespace TestNamespace
{
    public partial class Person1    
    {
        public readonly string name; 
        public readonly int age; 
        public readonly Job job; 
        public readonly IList<string> hobbies; 

        [JsonConstructor]
        public Person1(
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
