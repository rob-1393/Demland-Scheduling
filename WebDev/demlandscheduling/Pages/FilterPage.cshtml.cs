using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Linq;
using demlandscheduling.DataModels; // Your data models
using demlandscheduling.Data; // Your data context
namespace demlandscheduling.Pages.Shares.FilterPageModel;

public class FilterPageModel : PageModel
{
    private readonly ApplicationDbContext _context;

    public FilterPageModel(ApplicationDbContext context)
    {
        _context = context;
    }

    // The filter object that will hold all filter parameters from the user
    [BindProperty(SupportsGet = true)]
    public FilterModel Filter { get; set; }

    public List<DemlandData> Classes { get; set; }

    // OnGet method to filter data based on user input
    public void OnGet()
    {
        IQueryable<DemlandData> query = _context.DemlandData;

        // Apply filters dynamically if the user has entered values
        if (!string.IsNullOrEmpty(Filter.Course))
        {
            query = query.Where(c => c.Course.Contains(Filter.Course));
        }
        if (!string.IsNullOrEmpty(Filter.TeacherDescrip))
        {
            query = query.Where(c => c.TeacherDescrip.Contains(Filter.TeacherDescrip));
        }
        if (!string.IsNullOrEmpty(Filter.Days))
        {
            query = query.Where(c => c.Days.Contains(Filter.Days));
        }
        if (Filter.StartTime != null)
        {
            query = query.Where(c => c.StartTime >= Filter.StartTime);
        }
        if (Filter.EndTime != null)
        {
            query = query.Where(c => c.EndTime <= Filter.EndTime);
        }
        if (!string.IsNullOrEmpty(Filter.Email))
        {
            query = query.Where(c => c.Email.Contains(Filter.Email));
        }

        // Execute the query and retrieve the filtered data
        Classes = query.ToList();
    }
}

// Filter model that maps to the fields in the form
public class FilterModel
{
    public string? Course { get; set; }
    public string? TeacherDescrip { get; set; }
    public string? Days { get; set; }
    public TimeOnly? StartTime { get; set; }
    public TimeOnly? EndTime { get; set; }
    public string? Email { get; set; }
}
