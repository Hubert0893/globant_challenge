
-- Requirement 1
select b.department
	,c.job
	,case when DATEPART(QUARTER, a.datetime)=1 then COUNT(a.id) else 0 end Q1
	,case when DATEPART(QUARTER, a.datetime)=2 then COUNT(a.id) else 0 end Q2
	,case when DATEPART(QUARTER, a.datetime)=3 then COUNT(a.id) else 0 end Q3
	,case when DATEPART(QUARTER, a.datetime)=4 then COUNT(a.id) else 0 end Q4
	--,count(a.id) 
from  hired_employees a
inner join departments b on b.id = a.department_id
inner join jobs c on c.id = a.job_id
where year(cast(a.datetime as date)) = 2021
group by b.department,c.job,a.datetime
order by b.department asc,c.job asc;


-- Create a variable like average hired employees in 2021 for all departments
declare @avg_employees int = (select avg(total) from (select b.id, count(a.id) as total from  departments b
	inner join hired_employees a on b.id = a.department_id
	where year(cast(a.datetime as date)) = 2021
	group by b.id) c);

-- Requirement 2
select b.id
	,b.department
	,count(a.id) as hired
from  departments b
inner join hired_employees a on b.id = a.department_id
where year(cast(a.datetime as date)) = 2021
group by b.id,b.department 
having count(a.id)>@avg_employees
