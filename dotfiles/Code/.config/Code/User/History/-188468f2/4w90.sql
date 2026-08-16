-- create database test;
-- use test;
-- drop table Teachers;


-- Create Placement table
CREATE TABLE Placement (
    P_ID INT PRIMARY KEY,
    Dept VARCHAR(50),
    Place VARCHAR(50)
);


-- Insert data into Placement table
INSERT INTO Placement (P_ID, Dept, Place) VALUES
(1, 'Computer Science', 'Pune'),
(2, 'Data Science', 'Bangalore'),
(3, 'Mathematics', 'Delhi');

-- Create Teachers table
CREATE TABLE Teachers (
    T_ID INT PRIMARY KEY,
    Name VARCHAR(50),
    Age INT,
    Department VARCHAR(50),
    Date_of_Join DATE,
    Salary INT,
    Gender CHAR(1),
    HOD INT,
    FOREIGN KEY (Department) REFERENCES Placement(Dept),
    CHECK (Gender IN ('M', 'F'))
);

-- Insert data into Teachers table
INSERT INTO Teachers (T_ID, Name, Age, Department, Date_of_Join, Salary, Gender, HOD) VALUES
(1001, 'Somanth', 34, 'Computer Science', '2019-05-10', 60000, 'M', 1004),
(1002, 'Shiva', 42, 'Data Science', '2012-07-16', 80000, 'F', 1007),
(1003, 'Rajan', 32, 'Mathematics', '2021-08-18', 60000, 'M', 1006),
(1004, 'Roy', 38, 'Computer Science', '2017-11-21', 80000, 'F', 1004),
(1005, 'Samira', 28, 'Mathematics', '2023-04-27', 55000, 'M', 1006),
(1006, 'Randeep', 38, 'Mathematics', '2015-05-18', 75000, 'M', 1006),
(1007, 'Ramya', 48, 'Data Science', '2008-08-02', 100000, 'M', 1007),
(1008, 'Anitha', 32, 'Computer Science', '2021-08-18', 75000, 'F', 1004);

-- Output 1
SELECT 
    Department as Dept,
    ROUND(AVG(Salary), 2) as 'Avg (Salary)'
FROM 
    Teachers
GROUP BY 
    Department;

-- Output 2
SELECT 
    t.Name,
    t.Department,
    t.Salary,
    p.Place
FROM 
    Teachers t
JOIN 
    Placement p ON t.Department = p.Dept
WHERE 
    t.Salary <= 75000
ORDER BY 
    t.Department, t.Name;

-- Output 3
SELECT 
    t1.Name as 'Teacher_Name',
    t2.Name as 'HoD_Name'
FROM 
    Teachers t1
JOIN 
    Teachers t2 ON t1.HOD = t2.T_ID

