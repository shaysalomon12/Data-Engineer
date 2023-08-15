-- SQL Server Databases Inventory 
if object_id('tempdb..#t', 'U') is not null
drop table #t;
create table #t(
  ServerName varchar(128) default @@servername
, Version varchar(2000)
, DBName varchar(128) default db_name()
, DBOwner varchar(128)
, CreateDate datetime2
, RecoveryModel varchar(12) 
, StateDesc varchar(60)
, CompatibilityLevel int
, DataFileSizeMB int
, LogFileSizeMB int
, DataUsageMB int
, IndexUsageMB int
, SizeMB decimal(17,2)
, Collation varchar(60)
, UserCount int
, RoleCount int
, TableCount int
, SPCount int
, UDFCount int
, ViewCount int
, DMLTriggerCount int
, IsCaseSensitive bit
, IsTrustWorthy bit
, LastFullBackupDate datetime2
, LastDiffBackupDate datetime2
, LastLogBackupDate datetime2);

insert into #t(DBName, Version, DBOwner, CreateDate, RecoveryModel, StateDesc, CompatibilityLevel, IsCaseSensitive
, IsTrustWorthy, Collation, LastFullBackupDate, LastDiffBackupDate, LastLogBackupDate)
select name, @@version, suser_sname(owner_sid), create_date, recovery_model_desc, state_desc,compatibility_level
, IsCaseSensitive=CAST(CHARINDEX(N'_CS_', collation_name) AS bit), is_trustworthy_on, Collation_Name
, t.LastFullBackup, t.LastDiffBackup, t.LastLogBackup
from master.sys.databases db
outer apply( SELECT
MAX(CASE WHEN b.type = 'D' THEN b.backup_finish_date END) AS LastFullBackup,
MAX(CASE WHEN b.type = 'I' THEN b.backup_finish_date END) AS LastDiffBackup,
MAX(CASE WHEN b.type = 'L' THEN b.backup_finish_date END) AS LastLogBackup
FROM msdb.dbo.backupset b 
where b.database_name = db.name
) t;

EXEC master.dbo.sp_msforeachdb'use [?]
update t set SizeMB=(select sum(size)/128. from dbo.sysfiles)
, DataUsageMB=x.DataUsageMB, IndexUsageMB=x.IndexUsageMB
   , DataFileSizeMB = u.DBSize, LogFileSizeMB = u.LogSize 
   , TableCount=y.TC, UDFCount=y.UC, SPCount = y.SC, ViewCount=y.VC
   , DMLTriggerCount=y.DC
   , UserCount = z.UC, RoleCount = z.RC
from #t t
   outer apply (
   SELECT SUM(case when df.type in (0,2,4) then df.size else 0 end)/128
   , SUM(case when df.type in (1,3) then df.size else 0 end)/128 
   FROM sys.database_files df 
   ) u(DBSize, LogSize)
   outer apply(select  DataUsageMB=sum(
    CASE
    When it.internal_type IN (202,204,207,211,212,213,214,215,216,221,222,236) Then 0
    When a.type <> 1 and p.index_id < 2 Then a.used_pages
    When p.index_id < 2 Then a.data_pages
    Else 0
    END)/128,
IndexUsageMB=(sum(a.used_pages)-sum(
    CASE
    When it.internal_type IN (202,204,207,211,212,213,214,215,216,221,222,236) Then 0
    When a.type <> 1 and p.index_id < 2 Then a.used_pages
    When p.index_id < 2 Then a.data_pages
    Else 0
    END
    ))/128
    from sys.partitions p join sys.allocation_units a on p.partition_id = a.container_id
    left join sys.internal_tables it on p.object_id = it.object_id
   ) x
   outer apply 
   ( select SC=Sum(case Type when ''P'' then 1 else 0 end)
    , DC=Sum(case Type when ''TR'' then 1 else 0 end)
    , TC=Sum(case Type when ''U'' then 1 end)
    , UC= sum(case when Type in (''TF'', ''IF'', ''FN'') then 1 else 0 end)
    , VC=Sum(case Type when ''V'' then 1 else 0 end)
    from sys.objects where object_id > 1024
    and type in (''U'',''P'',''TR'',''V'',''TF'',''IF'',''FN'')
   ) y
   outer apply 
   ( select UC = sum(case when [Type] in (''G'',''S'',''U'') then 1 else 0 end)
      , RC = sum(case when Type = ''R'' then 1 else 0 end)
      from sys.database_principals
      where principal_id > 4
   ) z where t.DBName=db_name();
'
SELECT * FROM #t;
