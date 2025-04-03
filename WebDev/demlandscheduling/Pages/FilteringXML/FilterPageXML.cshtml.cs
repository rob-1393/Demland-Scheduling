using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Xml.Linq;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace demlandscheduling.Pages.FilteringXML
{
    public class FilterPageXML : PageModel
    {
        public List<Course> Courses { get; set; } = new List<Course>();
        public FilterModel Filter { get; set; } = new FilterModel();

        public void OnGet(string? Course, string? Instructor, string? StartTime, string? EndTime)
        {
            string xmlPath = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "FilterPageXML.xml");
            if (!System.IO.File.Exists(xmlPath))
            {
                Console.WriteLine($"XML file not found at {xmlPath}");
                return;
            }

            LoadCourses(xmlPath);

            // Store filter values
            Filter = new FilterModel
            {
                Course = Course,
                Instructor = Instructor,
                StartTime = string.IsNullOrWhiteSpace(StartTime) ? null : StartTime,
                EndTime = string.IsNullOrWhiteSpace(EndTime) ? null : EndTime
            };

            // Apply filtering based on filters
            Courses = Courses
                .Where(c =>
                    (string.IsNullOrEmpty(Filter.Course) || c.CourseCode.Equals(Filter.Course, StringComparison.OrdinalIgnoreCase)) &&
                    (string.IsNullOrEmpty(Filter.Instructor) || c.Instructor.Equals(Filter.Instructor, StringComparison.OrdinalIgnoreCase)) &&
                    (Filter.StartTime == null || (c.StartTime != null && string.Compare(c.StartTime, Filter.StartTime, StringComparison.Ordinal) >= 0)) &&
                    (Filter.EndTime == null || (c.EndTime != null && string.Compare(c.EndTime, Filter.EndTime, StringComparison.Ordinal) <= 0)))
                .ToList();

            // Populate ViewData for dropdowns
            ViewData["Courses"] = Courses.Select(c => c.CourseCode).Distinct().ToList();
            ViewData["Instructors"] = Courses.Select(c => c.Instructor).Distinct().ToList();
        }

        private void LoadCourses(string xmlPath)
        {
            XDocument xmlDoc = XDocument.Load(xmlPath);

            // Parse XML data into Course objects
            Courses = xmlDoc.Descendants("row")
                .Select(c => new Course
                {
                    CourseCode = (string?)c.Element("Course") ?? "N/A",  // Maps to <Course>
                    Section = (string?)c.Element("Section") ?? "N/A",  // Maps to <Section>
                    Title = (string?)c.Element("ClassSchedDescrip") ?? "Unknown",  // Maps to <ClassSchedDescrip>
                    Instructor = (string?)c.Element("TeacherDescrip") ?? "Unknown",  // Maps to <TeacherDescrip>
                    Days = (string?)c.Element("Days") ?? "N/A",  // Maps to <Days>
                    StartTime = (string?)c.Element("StartTime") ?? "N/A",  // Maps to <StartTime>
                    EndTime = (string?)c.Element("EndTime") ?? "N/A",  // Maps to <EndTime>
                    Credits = int.TryParse((string?)c.Element("Cr"), out int cr) ? cr : 0,  // Maps to <Cr>
                    MaxEnrollment = int.TryParse((string?)c.Element("Max"), out int max) ? max : 0  // Maps to <Max>
                })
                .ToList();

            Console.WriteLine($"Loaded {Courses.Count} courses from XML.");
        }

        public class Course
        {
            public string CourseCode { get; set; } = "N/A";  // Matches <Course>
            public string Section { get; set; } = "N/A";  // Matches <Section>
            public string Title { get; set; } = "Unknown";  // Matches <ClassSchedDescrip>
            public string Instructor { get; set; } = "Unknown";  // Matches <TeacherDescrip>
            public string Days { get; set; } = "N/A";  // Matches <Days>
            public string StartTime { get; set; } = "N/A";  // Matches <StartTime>
            public string EndTime { get; set; } = "N/A";  // Matches <EndTime>
            public int Credits { get; set; } = 0;  // Matches <Cr>
            public int MaxEnrollment { get; set; } = 0;  // Matches <Max>
        }

        public class FilterModel
        {
            public string? Course { get; set; }
            public string? Instructor { get; set; }
            public string? StartTime { get; set; }
            public string? EndTime { get; set; }
        }
    }
}
