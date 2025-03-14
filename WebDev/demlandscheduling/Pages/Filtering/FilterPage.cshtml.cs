using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Linq;
using demlandscheduling.DataModels; // Your data models
using demlandscheduling.Data; // Your data context
using Microsoft.Extensions.Logging; // For logging

namespace demlandscheduling.Pages.Filtering
{
    public class FilterPage : PageModel
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<FilterPage> _logger;

        // Constructor to inject the context and logger
        public FilterPage(ApplicationDbContext context, ILogger<FilterPage> logger)
        {
            _context = context;
            _logger = logger;
        }

        // The filter object that will hold all filter parameters from the user
        [BindProperty(SupportsGet = true)]
        public FilterModel? Filter { get; set; }

        public List<DemlandData>? Classes { get; set; }

        // OnGet method to filter data based on user input
        public void OnGet()
        {
            _logger.LogInformation($"Course filter value: {Filter?.Course}");

            // Initialize query to get all data
            IQueryable<DemlandData> query = _context.DemlandData;

            try
            {
                // Apply filters dynamically if the user has entered values
                if (!string.IsNullOrEmpty(Filter?.Course))
                {
                    query = query.Where(c => c.Course != null && c.Course.Contains(Filter.Course, StringComparison.OrdinalIgnoreCase));
                }

                if (!string.IsNullOrEmpty(Filter?.TeacherDescrip))
                {
                    query = query.Where(c => c.TeacherDescrip != null && c.TeacherDescrip.Contains(Filter.TeacherDescrip, StringComparison.OrdinalIgnoreCase));
                }

                if (!string.IsNullOrEmpty(Filter?.Days))
                {
                    query = query.Where(c => c.Days != null && c.Days.Contains(Filter.Days, StringComparison.OrdinalIgnoreCase));
                }

                // Filter by start time if provided
                if (Filter?.StartTime.HasValue == true)
                {
                    var startTime = Filter.StartTime.Value;
                    query = query.Where(c => c.StartTime >= startTime); // Adjust based on how your DB stores time
                }

                // Filter by end time if provided
                if (Filter?.EndTime.HasValue == true)
                {
                    var endTime = Filter.EndTime.Value;
                    query = query.Where(c => c.EndTime <= endTime); // Adjust based on your DB storage of time
                }

                if (!string.IsNullOrEmpty(Filter?.Email))
                {
                    query = query.Where(c => c.Email != null && c.Email.Contains(Filter.Email, StringComparison.OrdinalIgnoreCase));
                }

                // Filter by numeric fields
                if (Filter?.Cr > 0)
                {
                    query = query.Where(c => c.Cr == Filter.Cr);
                }

                if (Filter?.Max > 0)
                {
                    query = query.Where(c => c.Max == Filter.Max);
                }

                if (Filter?.Reg > 0)
                {
                    query = query.Where(c => c.Reg == Filter.Reg);
                }

                // Filter by other fields if provided
                if (!string.IsNullOrEmpty(Filter?.SchedID))
                {
                    query = query.Where(c => c.SchedID != null && c.SchedID.Contains(Filter.SchedID, StringComparison.OrdinalIgnoreCase));
                }

                if (!string.IsNullOrEmpty(Filter?.DeliveryMethod))
                {
                    query = query.Where(c => c.DeliveryMethod != null && c.DeliveryMethod.Contains(Filter.DeliveryMethod, StringComparison.OrdinalIgnoreCase));
                }

                if (!string.IsNullOrEmpty(Filter?.SecondaryTeachers))
                {
                    query = query.Where(c => c.SecondaryTeachers != null && c.SecondaryTeachers.Contains(Filter.SecondaryTeachers, StringComparison.OrdinalIgnoreCase));
                }

                if (Filter?.ClassStart.HasValue == true)
                {
                    query = query.Where(c => c.ClassStart >= Filter.ClassStart.Value);
                }

                if (Filter?.ClassEnd.HasValue == true)
                {
                    query = query.Where(c => c.ClassEnd <= Filter.ClassEnd.Value);
                }

                if (!string.IsNullOrEmpty(Filter?.ClassSchedDescrip))
                {
                    query = query.Where(c => c.ClassSchedDescrip != null && c.ClassSchedDescrip.Contains(Filter.ClassSchedDescrip, StringComparison.OrdinalIgnoreCase));
                }

                // Execute the query and retrieve the filtered data
                Classes = query.ToList();  // This will fetch the data from the database

                // Check if any data was found
                if (Classes == null || Classes.Count == 0)
                {
                    _logger.LogInformation("No classes found with the specified filters.");
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "An error occurred while filtering classes.");
                // Handle error, maybe show a friendly message to the user
            }
        }

        // Filter model that maps to the fields in the form
        public class FilterModel
        {
            public string? AgreementNumber { get; set; }
            public string? SchedID { get; set; }
            public string? DeliveryMethod { get; set; }
            public string? Course { get; set; }
            public string? Section { get; set; }
            public string? Days { get; set; }
            public TimeOnly? StartTime { get; set; }
            public TimeOnly? EndTime { get; set; }
            public int Cr { get; set; }  // Non-nullable if this value is always required
            public int Max { get; set; } // Non-nullable if this value is always required
            public int Reg { get; set; } // Non-nullable if this value is always required
            public string? TeacherDescrip { get; set; }
            public string? Email { get; set; }
            public string? SecondaryTeachers { get; set; }
            public DateTime? ClassStart { get; set; }
            public DateTime? ClassEnd { get; set; }
            public string? ClassSchedDescrip { get; set; }
        }
    }
}
