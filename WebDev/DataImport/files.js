const sql = require('mssql');
const fs = require('fs');
const csv = require('csv-parser');
const config = require('./config'); // Import the database configuration

// Function to import data from a CSV file
async function importCSVData(filePath) {
    try {
        // Connect to SQL Server
        await sql.connect(config);

        // Read and parse the CSV file
        fs.createReadStream(filePath)
            .pipe(csv())
            .on('data', async (row) => {
                const { AgreementNumber, SchedID, DeliveryMethod, Course, Section, Days, StartTime, EndTime, Cr, Max, Reg, TeacherDescrip, Email, SecondaryTeachers, ClassStart, ClassEnd, ClassSchedDescrip } = row;
                await sql.query(`
                    INSERT INTO DemlandData (AgreementNumber, SchedID, DeliveryMethod, Course, Section, Days, StartTime, EndTime, Cr, Max, Reg, TeacherDescrip, Email, SecondaryTeachers, ClassStart, ClassEnd, ClassSchedDescrip)
                    VALUES ('${AgreementNumber}', '${SchedID}', '${DeliveryMethod}', '${Course}', '${Section}', '${Days}', '${StartTime}', '${EndTime}', '${Cr}', '${Max}', '${Reg}', '${TeacherDescrip}', '${Email}', '${SecondaryTeachers}', '${ClassStart}', '${ClassEnd}', '${ClassSchedDescrip}')
                `);
            })
            .on('end', () => {
                console.log('CSV data imported successfully!');
            });
    } catch (err) {
        console.error('Error importing CSV data: ', err);
    }
}

// Call the function with the path to your CSV file
importCSVData("C:\\Users\\Mbarn\\OneDrive\\Desktop\\demlanddata.csv");
