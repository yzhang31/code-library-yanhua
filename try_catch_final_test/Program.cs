using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace try_catch_final_test
{
    class Program
    {
        static void Main(string[] args)
        {
            tryfinalTest();
        }

        static void tryfinalTest()
        {
            try
            {
                Console.WriteLine("tryfinalTest - try called.");
                return;
            }
            finally
            {
                Console.WriteLine("tryfinalTest - finally called.");
            }
        }
    }
}
