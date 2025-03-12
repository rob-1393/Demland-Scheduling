using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Linq;
using demlandscheduling.DataModels; // Your data models
using demlandscheduling.Data; // Your data context
using System.Globalization;

namespace demlandscheduling.Pages.Shares
{
    public class FilterPageModel : PageModel
    {
        private readonly ApplicationDbContext _context;

        // Constructor to inject the context
        public FilterPageModel(ApplicationDbContext context)
        {
            _context = context;
        }

        // The filter object that will hold all filter parameters from the user
        [BindProperty(SupportsGet = true)]
        public FilterModel? Filter { get; set; }

        public List<DemlandData>? Classes { get; set; }

        // OnGet method to filter data based on user input
        public void OnGet()
        {
            IQueryable<DemlandData> query = _context.DemlandData;

            // Apply filters dynamically if the user has entered values
            if (!string.IsNullOrEmpty(Filter?.Course))
            {
                query = query.Where(c => c.Course.Contains(Filter.Course, StringComparison.OrdinalIgnoreCase));
            }

            if (!string.IsNullOrEmpty(Filter?.TeacherDescrip))
            {
                query = query.Where(c => c.TeacherDescrip.Contains(Filter.TeacherDescrip, StringComparison.OrdinalIgnoreCase));
            }

            if (!string.IsNullOrEmpty(Filter?.Days))
            {
                query = query.Where(c => c.Days.Contains(Filter.Days, StringComparison.OrdinalIgnoreCase));
            }

            // Filter by start time if provided
            if (Filter?.StartTime.HasValue == true)
            {
                var startTime = Filter.StartTime.Value;
                query = query.Where(c => c.StartTime >= startTime);
            }

            // Filter by end time if provided
            if (Filter?.EndTime.HasValue == true)
            {
                var endTime = Filter.EndTime.Value;
                query = query.Where(c => c.EndTime <= endTime);
            }

            if (!string.IsNullOrEmpty(Filter?.Email))
            {
                query = query.Where(c => c.Email.Contains(Filter.Email, StringComparison.OrdinalIgnoreCase));
            }

            // Execute the query and retrieve the filtered data
            Classes = query.ToList();
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
        public int Cr { get; set; }
        public int Max { get; set; }
        public int Reg { get; set; }
        public string? TeacherDescrip { get; set; }
        public string? Email { get; set; }
        public string? SecondaryTeachers { get; set; }
        public DateTime? ClassStart { get; set; }
        public DateTime? ClassEnd { get; set; }
        public string? ClassSchedDescrip { get; set; }
    }
}
