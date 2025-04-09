using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Xml.Linq;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace demlandscheduling.Pages.Index
{
    public class IndexModel : PageModel
    {
        public List<Course> Courses { get; set; } = new();

        public string SortOrder { get; set; } = "None";
        public string SortStartTime { get; set; } = "None";
        public string SortEndTime { get; set; } = "None";
        public string SortCredits { get; set; } = "None";
        public string SortMaxEnrollment { get; set; } = "None";
        public string SortCourseCode { get; set; } = "None";

        public void OnGet(string? sortStartTime, string? sortEndTime, string? sortCredits, string? sortMaxEnrollment, string? sortCourseCode)
        {
            string xmlPath = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "FilterPageXML.xml");
            if (!System.IO.File.Exists(xmlPath))
            {
                Console.WriteLine($"XML file not found at {xmlPath}");
                return;
            }

            LoadCourses(xmlPath);

            // Apply sorting
            if (!string.IsNullOrEmpty(sortCourseCode))
            {
                SortCourseCode = sortCourseCode;
                Courses = sortCourseCode switch
                {
                    "Ascending" => Courses.OrderBy(c => c.CourseCode).ToList(),
                    "Descending" => Courses.OrderByDescending(c => c.CourseCode).ToList(),
                    _ => Courses
                };
            }

            if (!string.IsNullOrEmpty(sortStartTime))
            {
                SortStartTime = sortStartTime;
                Courses = sortStartTime switch
                {
                    "Ascending" => Courses.OrderBy(c => ParseTime(c.StartTime)).ToList(),
                    "Descending" => Courses.OrderByDescending(c => ParseTime(c.StartTime)).ToList(),
                    _ => Courses
                };
            }

            if (!string.IsNullOrEmpty(sortEndTime))
            {
                SortEndTime = sortEndTime;
                Courses = sortEndTime switch
                {
                    "Ascending" => Courses.OrderBy(c => ParseTime(c.EndTime)).ToList(),
                    "Descending" => Courses.OrderByDescending(c => ParseTime(c.EndTime)).ToList(),
                    _ => Courses
                };
            }

            if (!string.IsNullOrEmpty(sortCredits))
            {
                SortCredits = sortCredits;
                Courses = sortCredits switch
                {
                    "Ascending" => Courses.OrderBy(c => c.Credits).ToList(),
                    "Descending" => Courses.OrderByDescending(c => c.Credits).ToList(),
                    _ => Courses
                };
            }

            if (!string.IsNullOrEmpty(sortMaxEnrollment))
            {
                SortMaxEnrollment = sortMaxEnrollment;
                Courses = sortMaxEnrollment switch
                {
                    "Ascending" => Courses.OrderBy(c => c.MaxEnrollment).ToList(),
                    "Descending" => Courses.OrderByDescending(c => c.MaxEnrollment).ToList(),
                    _ => Courses
                };
            }
        }

        private void LoadCourses(string xmlPath)
        {
            XDocument xmlDoc = XDocument.Load(xmlPath);

            Courses = xmlDoc.Descendants("row")
                .Select(c => new Course
                {
                    CourseCode = (string?)c.Element("Course") ?? "N/A",
                    Section = (string?)c.Element("Section") ?? "N/A",
                    Title = (string?)c.Element("ClassSchedDescrip") ?? "Unknown",
                    Instructor = (string?)c.Element("TeacherDescrip") ?? "Unknown",
                    Days = (string?)c.Element("Days") ?? "N/A",
                    StartTime = (string?)c.Element("StartTime") ?? "N/A",
                    EndTime = (string?)c.Element("EndTime") ?? "N/A",
                    Credits = int.TryParse((string?)c.Element("Cr"), out int cr) ? cr : 0,
                    MaxEnrollment = int.TryParse((string?)c.Element("Max"), out int max) ? max : 0
                })
                .ToList();
        }

        private static DateTime ParseTime(string? time)
        {
            return DateTime.TryParse(time, out var parsed) ? parsed : DateTime.MinValue;
        }

        public class Course
        {
            public string CourseCode { get; set; } = "N/A";
            public string Section { get; set; } = "N/A";
            public string Title { get; set; } = "Unknown";
            public string Instructor { get; set; } = "Unknown";
            public string Days { get; set; } = "N/A";
            public string StartTime { get; set; } = "N/A";
            public string EndTime { get; set; } = "N/A";
            public int Credits { get; set; }
            public int MaxEnrollment { get; set; }
        }
    }
}