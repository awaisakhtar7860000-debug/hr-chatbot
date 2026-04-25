-- ================================================
-- HR Chatbot Database Schema
-- Supabase SQL Editor mein copy-paste karein
-- ================================================

-- 1. Employees Table
CREATE TABLE employees (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,  -- Format: +923001234567
    employee_id VARCHAR(20) UNIQUE,
    department VARCHAR(50),
    designation VARCHAR(100),
    joining_date DATE,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 2. Policies Table (HR Policy + Labor Law content)
CREATE TABLE policies (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50),  -- leave, overtime, salary, attendance, general
    source VARCHAR(100),   -- "Company Policy" ya "Factories Act 1934"
    effective_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. Forms Table
CREATE TABLE forms (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    form_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    file_path VARCHAR(200),  -- local path: forms/annual_leave_form.pdf
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 4. Chat Logs Table (audit ke liye)
CREATE TABLE chat_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    employee_phone VARCHAR(20),
    employee_name VARCHAR(100),
    message TEXT,
    bot_response TEXT,
    was_in_scope BOOLEAN,
    form_sent VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ================================================
-- Sample Data Insert
-- ================================================

-- Test employees (apne actual employees add karein)
INSERT INTO employees (name, phone, employee_id, department, designation) VALUES
('Ali Hassan', '+923001234567', 'EMP001', 'IT', 'Software Developer'),
('Sara Ahmed', '+923009876543', 'EMP002', 'Finance', 'Accountant'),
('Usman Khan', '+923451234567', 'EMP003', 'HR', 'HR Officer');

-- Sample policies
INSERT INTO policies (title, content, category, source) VALUES
(
    'Annual Leave Policy',
    'Har employee ko saal mein 14 din ki annual leave milti hai. Yeh leave 1 saal ki service poori hone ke baad milti hai. Annual leave carry forward ho sakti hai lekin maximum 28 din tak. Leave apply karne ke liye 3 din pehle manager ko batana zaroori hai.',
    'leave',
    'Company Policy 2024'
),
(
    'Casual Leave Policy',
    'Casual leave 10 din per saal hoti hai. Yeh leave encash nahi hoti aur carry forward bhi nahi hoti. Same day ya 1 din pehle apply kar saktay hain. Emergency mein phone pe bhi inform kar saktay hain.',
    'leave',
    'Company Policy 2024'
),
(
    'Overtime Rules',
    'Normal working hours 8 ghante per din aur 48 ghante per hafte hain. Overtime ke liye double rate milta hai. Pehle manager se approval lena zaroori hai. Monthly maximum 50 ghante overtime allowed hai.',
    'overtime',
    'Factories Act 1934 + Company Policy'
),
(
    'Salary Policy',
    'Salary har mahine ki 25 tarikh ko bank mein transfer hoti hai. Agar 25 Saturday ya Sunday ho to previous working day ko milegi. Salary slip WhatsApp pe ya HR portal pe available hoti hai.',
    'salary',
    'Company Policy 2024'
),
(
    'Medical Leave',
    'Sick leave 10 din per saal hai. 2 din se zyada bimari mein registered doctor ka certificate zaroori hai. Serious bimari mein additional unpaid leave bhi mil sakti hai management approval se.',
    'leave',
    'West Pakistan Sick Leave Rules + Company Policy'
);

-- Sample forms record
INSERT INTO forms (form_name, category, file_path, description) VALUES
('Annual Leave Form', 'leave', 'forms/annual_leave_form.pdf', 'Annual/earned leave application form'),
('Casual Leave Form', 'leave', 'forms/casual_leave_form.pdf', 'Casual leave application form'),
('Medical Leave Form', 'leave', 'forms/sick_leave_form.pdf', 'Sick/medical leave with doctor certificate'),
('Overtime Form', 'overtime', 'forms/overtime_form.pdf', 'Overtime request and approval form'),
('Salary Certificate', 'salary', 'forms/salary_certificate_request.pdf', 'Request for salary certificate'),
('Resignation Form', 'general', 'forms/resignation_form.pdf', 'Formal resignation letter template');
