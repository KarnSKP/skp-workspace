using System;
using System.Globalization;

namespace Prime
{
    class Program
    {
        static void Main(string[] args)
        {
            int START = Convert.ToInt32(Console.ReadLine());
            int END = Convert.ToInt32(Console.ReadLine());
            bool IS_PRIME;
            
            for (int NUM = START; NUM <= END; NUM++)
            {
                IS_PRIME = true;
                for (int i = 2; i < NUM; i++)
                {
                    if (NUM % i == 0)
                    {
                        IS_PRIME = !IS_PRIME;
                        break;
                    }
                }
                if (IS_PRIME && NUM != 1)
                {
                    Console.WriteLine(NUM);
                }

            }
        }
    }
}
