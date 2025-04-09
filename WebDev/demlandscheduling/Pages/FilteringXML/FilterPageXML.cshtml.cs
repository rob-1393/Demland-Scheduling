using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Xml.Linq;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace demlandscheduling.Pages.FilteringXML
{
    public class FilterPageXML : PageModel //Powers the /FilteringXMl/FilterPageXML Razor page.
    {
        public List<Course> Courses { get; set; } = new List<Course>();
        public FilterModel Filter { get; set; } = new FilterModel();

        public string SortOrder { get; set; } = "None"; // Public string sort tracks the sorting state.
        public string SortMaxEnrollment { get; set; } = "None";
        public string SortStartTime { get; set; } = "None";
        public string SortEndTime { get; set; } = "None";
        public string SortCredits { get; set; } = "None";
// Below in public void loads the XML file fromn the wwwroot folder, parses the course records from XML into Course objects, stores filter values passed in the URL, sorts the list based on our sorting parameters and will lastly save the dropdown values in Viewdata.
        public void OnGet(
            string? Course, string? Instructor, string? StartTime, string? EndTime,
            string? sortOrder, string? sortMaxEnrollment, string? sortStartTime, string? sortEndTime, string? sortCredits)
        {
            string xmlPath = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "FilterPageXML.xml");
            if (!System.IO.File.Exists(xmlPath))
            {
                Console.WriteLine($"XML file not found at {xmlPath}");
                return;
            }

            LoadCourses(xmlPath);

            Filter = new FilterModel
            {
                Course = Course,
                Instructor = Instructor,
                StartTime = string.IsNullOrWhiteSpace(StartTime) ? null : StartTime,
                EndTime = string.IsNullOrWhiteSpace(EndTime) ? null : EndTime
            };

            Courses = Courses
                .Where(c =>
                    (string.IsNullOrEmpty(Filter.Course) || c.CourseCode.Equals(Filter.Course, StringComparison.OrdinalIgnoreCase)) &&
                    (string.IsNullOrEmpty(Filter.Instructor) || c.Instructor.Equals(Filter.Instructor, StringComparison.OrdinalIgnoreCase)) &&
                    (Filter.StartTime == null || (c.StartTime != null && string.Compare(c.StartTime, Filter.StartTime, StringComparison.Ordinal) >= 0)) &&
                    (Filter.EndTime == null || (c.EndTime != null && string.Compare(c.EndTime, Filter.EndTime, StringComparison.Ordinal) <= 0)))
                .ToList();

            if (sortOrder != null) SortOrder = sortOrder;
            if (sortMaxEnrollment != null) SortMaxEnrollment = sortMaxEnrollment;
            if (sortStartTime != null) SortStartTime = sortStartTime;
            if (sortEndTime != null) SortEndTime = sortEndTime;
            if (sortCredits != null) SortCredits = sortCredits;

            ApplySorting();

            ViewData["Courses"] = Courses.Select(c => c.CourseCode).Distinct().ToList();
            ViewData["Instructors"] = Courses.Select(c => c.Instructor).Distinct().ToList();
        }

        private void LoadCourses(string xmlPath) // Loads the XML file from disk and converts each row in the XML into a course cobject.
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

            Console.WriteLine($"Loaded {Courses.Count} courses from XML.");
        }

        private void ApplySorting() // Applies sorting logic based on the current sort selections
        {
            if (SortOrder == "Ascending")
                Courses = Courses.OrderBy(c => c.CourseCode).ThenBy(c => int.TryParse(c.CourseCode.Split('-')[1], out var n) ? n : int.MaxValue).ToList();
            else if (SortOrder == "Descending")
                Courses = Courses.OrderByDescending(c => c.CourseCode).ThenByDescending(c => int.TryParse(c.CourseCode.Split('-')[1], out var n) ? n : int.MinValue).ToList();

            if (SortMaxEnrollment == "Ascending")
                Courses = Courses.OrderBy(c => c.MaxEnrollment).ToList();
            else if (SortMaxEnrollment == "Descending")
                Courses = Courses.OrderByDescending(c => c.MaxEnrollment).ToList();

            if (SortStartTime == "Ascending")
                Courses = Courses.OrderBy(c => c.StartTime).ToList();
            else if (SortStartTime == "Descending")
                Courses = Courses.OrderByDescending(c => c.StartTime).ToList();

            if (SortEndTime == "Ascending")
                Courses = Courses.OrderBy(c => c.EndTime).ToList();
            else if (SortEndTime == "Descending")
                Courses = Courses.OrderByDescending(c => c.EndTime).ToList();

            if (SortCredits == "Ascending")
                Courses = Courses.OrderBy(c => c.Credits).ToList();
            else if (SortCredits == "Descending")
                Courses = Courses.OrderByDescending(c => c.Credits).ToList();
        }

        public class Course // Defines our structure for one course and etc.
        {
            public string CourseCode { get; set; } = "N/A";
            public string Section { get; set; } = "N/A";
            public string Title { get; set; } = "Unknown";
            public string Instructor { get; set; } = "Unknown";
            public string Days { get; set; } = "N/A";
            public string StartTime { get; set; } = "N/A";
            public string EndTime { get; set; } = "N/A";
            public int Credits { get; set; } = 0;
            public int MaxEnrollment { get; set; } = 0;
        }

        public class FilterModel //Holds the values the user selected in the filter form on the page.
        {
            public string? Course { get; set; }
            public string? Instructor { get; set; }
            public string? StartTime { get; set; }
            public string? EndTime { get; set; }
        }
    }
}
