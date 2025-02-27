namespace demlandscheduling.DataModels
{
    public class CourseData
    {
        public int Id {get; set; } //maps to the Id column in the CourseData table
        public string? Coursename {get; set;} //maps to the CourseName coulumn in the CourseData table
        public string? Instructor {get; set;} //maps to the Instructor column in the CourseData table
    }
}
