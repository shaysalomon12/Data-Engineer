rem #############################################################################
rem Shell script to take incremental level 0 backup
rem
rem usage: c:\> <script_name> <oracle_sid> <oracle_home>
rem
rem Backup file names:
rem %d - Database name
rem %T - 8-character name constituted by compressed representations of the backup 
rem      set or image copy number and the time the backup set or image copy was 
rem      created.
rem %t - Backup set time stamp,
rem %U - A system-generated unique filename (default).
rem #############################################################################

SET ORACLE_SID  = %1
SET ORACLE_HOME = %2

SET scripts_dir = d:\orascripts
SET backup_dir = \\share_name\%computername%\%ORACLE_SID%\

%ORACLE_HOME%\bin\rman target / cmdfile=%scripts_dir%\rman_incremental_level_0.cmd log=%backup_dir%\rman_incremental_level_0.log

rem ################## Incremental Level 0 ########################################
RMAN> run
{
ALLOCATE CHANNEL CH1 DEVICE TYPE DISK FORMAT '%backup_dir%\%d_level_0_%T_%t_%U';              ## Suggested
ALLOCATE CHANNEL CH2 DEVICE TYPE DISK FORMAT '%backup_dir%\%d_level_0_%U';
BACKUP tag 'INCR_LEVEL0_DB' INCREMENTAL LEVEL=0 AS COMPRESSED BACKUPSET DATABASE PLUS ARCHIVELOG;
BACKUP CURRENT CONTROLFILE TAG 'INCR_LEVEL0_CTL' FORMAT '%backup_dir%\%d_level_0_CTL_%U';
BACKUP SPFILE TAG 'INCR_LEVEL0_SPFILE' FORMAT '%backup_dir%\%d_level_0_SPF_%U';
RELEASE CHANNEL CH1;
RELEASE CHANNEL CH2;
}

rem ################## Incremental Cumulative LEVEL 1 ############################
RMAN> run
{
ALLOCATE CHANNEL CH1 DEVICE TYPE DISK FORMAT '%backup_dir%\%d_level_1_%U';
ALLOCATE CHANNEL CH2 DEVICE TYPE DISK FORMAT '%backup_dir%\%d_level_1_%U';
BACKUP tag 'INCR_CUMUL1_DB' INCREMENTAL LEVEL=1 CUMULATIVE AS COMPRESSED BACKUPSET DATABASE PLUS ARCHIVELOG;
BACKUP CURRENT CONTROLFILE TAG 'INCR_CUMUL1_CTL' FORMAT '%backup_dir%\%d_level_1_CTL_%U';
BACKUP SPFILE TAG 'INCR_CUMUL1_SPFILE' FORMAT '%backup_dir%\%d_level_1_SPF_%U';
RELEASE CHANNEL CH1;
RELEASE CHANNEL CH2;
}
