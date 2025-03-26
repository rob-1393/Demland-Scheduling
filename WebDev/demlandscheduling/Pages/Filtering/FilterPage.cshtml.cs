using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using System.Linq;
using demlandscheduling.DataModels;
using demlandscheduling.Data;


namespace demlandscheduling.Pages.Filtering
{
    public class FilterPage : PageModel
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<FilterPage> _logger;

        public FilterPage(ApplicationDbContext context, ILogger<FilterPage> logger)
        {
            _context = context;
            _logger = logger;
        }

        [BindProperty(SupportsGet = true)]
        public FilterModel? Filter { get; set; }

        public List<DemlandData>? Classes { get; set; }

        public void OnGet()
        {
            _logger.LogInformation($"Filtering data with the filter values: {Filter?.TeacherDescrip}, {Filter?.Course}, {Filter?.Cr}, {Filter?.StartTime}, {Filter?.EndTime}");

            IQueryable<DemlandData> query = _context.DemlandData;

            // Fetch distinct values for filtering options
            ViewData["Courses"] = _context.DemlandData.Select(d => d.Course).Distinct().ToList();
            ViewData["Teachers"] = _context.DemlandData.Select(d => d.TeacherDescrip).Distinct().ToList();
            ViewData["StartTime"] = _context.DemlandData.Select(d => d.StartTime).Distinct().ToList();
            ViewData["EndTime"] = _context.DemlandData.Select(d => d.EndTime).Distinct().ToList();

            // Keeping the other fields in ViewData for display
            ViewData["Days"] = _context.DemlandData.Select(d => d.Days).Distinct().ToList();
            ViewData["DeliveryMethods"] = _context.DemlandData.Select(d => d.DeliveryMethod).Distinct().ToList();
            ViewData["Email"] = _context.DemlandData.Select(d => d.Email).Distinct().ToList();
            ViewData["Max"] = _context.DemlandData.Select(d => d.Max).Distinct().ToList();
            ViewData["Reg"] = _context.DemlandData.Select(d => d.Reg).Distinct().ToList();
            ViewData["SchedID"] = _context.DemlandData.Select(d => d.SchedID).Distinct().ToList();
            ViewData["SecondaryTeachers"] = _context.DemlandData.Select(d => d.SecondaryTeachers).Distinct().ToList();
            ViewData["ClassStart"] = _context.DemlandData.Select(d => d.ClassStart).Distinct().ToList();
            ViewData["ClassEnd"] = _context.DemlandData.Select(d => d.ClassEnd).Distinct().ToList();
            ViewData["ClassSchedDescrip"] = _context.DemlandData.Select(d => d.ClassSchedDescrip).Distinct().ToList();

            try
            {
                // Apply filters based on user input for each field
                if (!string.IsNullOrEmpty(Filter?.Course))
                {
                    query = query.Where(c => c.Course != null && EF.Functions.Like(c.Course, "%" + Filter.Course + "%"));
                }

                if (!string.IsNullOrEmpty(Filter?.TeacherDescrip))
                {
                    query = query.Where(c => c.TeacherDescrip != null && EF.Functions.Like(c.TeacherDescrip, "%" + Filter.TeacherDescrip + "%"));
                }

                if (Filter?.StartTime.HasValue == true)
                {
                    var startTime = Filter.StartTime.Value;
                    query = query.Where(c => c.StartTime != null && c.StartTime >= startTime);
                }

                if (Filter?.EndTime.HasValue == true)
                {
                    var endTime = Filter.EndTime.Value;
                    query = query.Where(c => c.EndTime != null && c.EndTime <= endTime);
                }

                // Execute the query to retrieve the filtered data
                Classes = query.ToList();

                // Log if no data is found
                if (Classes == null || Classes.Count == 0)
                {
                    _logger.LogInformation("No classes found with the specified filters.");
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "An error occurred while filtering classes.");
            }
        }

        public class FilterModel
        {
            public string? Course { get; set; }
            public string? TeacherDescrip { get; set; }
            public TimeOnly? StartTime { get; set; }
            public TimeOnly? EndTime { get; set; }
            public int Cr { get; set; }
        }
    }
}
