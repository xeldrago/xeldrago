using System;

namespace DpadStickToggle
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("D-Pad -> Left Stick Remapper (Toggle Mode - L3 to toggle)\n");
            var mapper = new DpadMapper();
            mapper.Run();
        }
    }
}
