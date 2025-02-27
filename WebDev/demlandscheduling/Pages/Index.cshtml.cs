using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using demlandscheduling.Data;  // Correct namespace for ApplicationDbContext
using demlandscheduling.DataModels;  // Correct namespace for CourseData

namespace demlandscheduling.Pages.Courses
{
    public class IndexModel(ApplicationDbContext context) : PageModel
    {
        private readonly ApplicationDbContext _context = context;

        public IList<CourseData>? Courses { get; set; }

        public async Task OnGetAsync()
        {
            // Fetch all courses from the 'CourseData' table in SQL Server
            Courses = await _context.CourseData.ToListAsync();
        }
    }
}
