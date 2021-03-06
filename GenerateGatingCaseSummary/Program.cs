﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Text.RegularExpressions;

namespace GenerateGatingCaseSummary
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Count() == 0)
            {
                Console.WriteLine("Please provide a folder as command line parameter.");
                return;
            }

            string rootDir = args[0];
            if (!Directory.Exists(rootDir))
            {
                Console.WriteLine("Folder {0} is not existed.", rootDir);
                return;
            }
            Console.WriteLine("Scan folder:  " + rootDir);
            Dictionary<string, List<String>> summary = new Dictionary<string, List<String>>();
            IList<String> dirs = getAllMatchChildFolders(rootDir);

            Console.WriteLine("Analyzing.. ");
            getCaseInfo(summary, dirs);

            string outputFileName = "D:\\gating_algorithm_summary.csv";
            
            Console.WriteLine("Generating report file as " + outputFileName);
            
            generateReportFile(outputFileName, summary);

            Console.WriteLine("Finished. Generating report file as " + outputFileName);

        }

        private static void generateReportFile(string outputFileName, Dictionary<string, List<String>> summary)
        {
            using (TextWriter streamWriter = new StreamWriter(outputFileName))
            {
                streamWriter.WriteLine("Algorithm,Domain,Channel Code,Channel Type,Data Type,Sampling Rate,Case Name");
                foreach (var item in summary)
                {
                    foreach (var line in item.Value)
                    {
                        streamWriter.WriteLine(line);
                    }
                }
            }
        }
        private static void getCaseInfo(Dictionary<string, List<String>> summary, IList<String> dirs)
        {
            string channelCode, domainCode, caseName, dataType, channelType, samplingType;
            IList<String> algorithms;
            foreach (var casePath in dirs)
            {
                channelCode = getFirstMatchPatternString(casePath, @"\\([A-Za-z0-9\-_\+]+)\[");
                channelType = getFirstMatchPatternString(casePath, @"\[([0-9]+)\-");
                dataType = getFirstMatchPatternString(casePath, @"\-([A-Z0-9_]+)\]");
                domainCode = getDomainInfo(casePath);
                caseName = casePath.Split(new string[]{@"\"}, StringSplitOptions.RemoveEmptyEntries).Last();
                samplingType = getSamplingRate(casePath);
                algorithms = analyzeAlgorithms(casePath);

                foreach (var algorithm in algorithms)
                {
                    string line = string.Format("{0},{1},{2},{3},{4},{5},{6}", algorithm, domainCode, channelCode, channelType, dataType, samplingType, caseName );
                    if (!summary.ContainsKey(algorithm))
                    {
                        summary[algorithm] = new List<string>();
                    }
                    summary[algorithm].Add(line);
                }
            }
        }

        static string getDomainInfo(string casePath)
        {
            string result = string.Empty;
            if (casePath.Contains(")DEPTH[") || casePath.Contains("=DEPTH["))
            {
                result = "DEPTH";
            }

            if (casePath.Contains(")TIME[") || casePath.Contains("=TIME[") )
            {
                result += "/TIME";
            }
            return result;
        }

        static string getSamplingRate(string casePath)
        {
            string result = string.Empty;
            string pattern = @"([0-9.\[\]]+)@";
            var matches = Regex.Matches(casePath, pattern, RegexOptions.Singleline);
            foreach (Match match in matches)
            {
                result += match.Groups[1].Value;
            }
            return result;
        }

        static List<String> getAllMatchChildFolders(string rootPath)
        {

            string caseFolderPattern = "Direct.*@(OS_.*)$";
            // Dir directory recursively and filter each of line, then redirect to file, final exit to close cmd.exe.
            string cmdText ="dir /a:d /s \"{0}\" | findstr /I \"{1}\" > {2}&&exit";  
            string tempOutputFile = Path.GetTempFileName();

            string dosCommand = string.Format(cmdText, rootPath, caseFolderPattern, tempOutputFile);

            System.Diagnostics.Process p = System.Diagnostics.Process.Start("CMD.exe", "/c " + dosCommand);

            p.WaitForExit();

            List<String> lines = new List<string>();
            StreamReader strReader = new StreamReader(tempOutputFile);
            string line;
            while ((line = strReader.ReadLine()) != null)
            {
                lines.Add(line.Replace("Directory of",string.Empty).Trim());
            }
            strReader.Close();
            return lines;
        }
        static string getFirstMatchPatternString(string inputString, string pattern)
        {
            var match = Regex.Match(inputString, pattern, RegexOptions.Singleline);
            return match.Success ? match.Groups[1].Value : string.Empty;
        }

        static IList<string> analyzeAlgorithms(string gateCasePath)
        {
            HashSet<String> algorithms = new HashSet<String>();
            string channelNamePattern = @"\(([A-Za-z_]+)\)";
            var matches = Regex.Matches(gateCasePath, channelNamePattern, RegexOptions.Singleline);
            foreach (Match match in matches)
            {
                algorithms.Add(match.Groups[1].Value);
            }
            return algorithms.ToList();
        }
    }
}
