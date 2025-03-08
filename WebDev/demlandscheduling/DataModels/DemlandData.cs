namespace demlandscheduling.DataModels
{
    public class DemlandData
    {
        public string? AgreementNumber {get; set; } //maps to the AgreementNumber column in the DemlandData table
        public string? SchedID {get; set;} //maps to the SchedID coulumn in the DemlandData table
        public string? DeliveryMethod {get; set;} //maps to the DeliveryMethod column in the DemlandData table
        public string? Course {get; set; } //maps to the Course column in the DemlandData table
        public string? Section {get; set;} //maps to the Section coulumn in the DemlandData table
        public string? Days {get; set;} //maps to the Days column in the DemlandData table
        public TimeOnly? StartTime {get; set; } //maps to the StartTime column in the DemlandData table
        public TimeOnly? EndTime {get; set;} //maps to the EndTime coulumn in the DemlandData table
        public int Cr {get; set;} //maps to the Cr column in the DemlandData table
        public int Max {get; set; } //maps to the Max column in the DemlandData table
        public int Reg {get; set;} //maps to the Reg coulumn in the DemlandData table
        public string? TeacherDescrip {get; set;} //maps to the TeacherDescrip column in the DemlandData table
        public string? Email {get; set;} //maps to the Email column in the DemlandData table
        public string? SecondaryTeachers {get; set; } //maps to the SecondaryTeachers column in the DemlandData table
        public DateTime? ClassStart {get; set;} //maps to the ClassStart coulumn in the DemlandData table
        public DateTime? ClassEnd {get; set;} //maps to the ClassEnd column in the DemlandData table
        public string? ClassSchedDescrip {get; set; } //maps to the ClassSchedDescrip column in the DemlandData table
    }
}
