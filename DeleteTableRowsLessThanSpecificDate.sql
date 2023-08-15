CREATE PROCEDURE [dbo].[DeleteTableRowsLessThanSpecificDate] 
	@RetentionDays INT,
	@RowsToDelete INT,
	@SchemaName SYSNAME,
    @TableName SYSNAME,
	@ColumnName SYSNAME
AS
BEGIN
/* --------------------------------------------------------------------
@RetentionDays 	- How many days to keep in the table
@RowsToDelete 	- No. of records to delete each time we run this SP
@SchemaName 	- Schema where the table we want to delete
@TableName 		- Table name we want to delete
@ColumnName 	- Column name we use to compare the date to delete

To automate the delete process, create SQL Agent Job to scheduled once a week running:

EXEC dbo.DeleteTableRowsLessThanSpecificDate
	@RetentionDays = 100,
    @RowsToDelete = 1000000,
    @SchemaName = 'dbo',
	@TableName = 'DevErrorLog',
	@ColumnName = 'timestamp'
GO
-------------------------------------------------------------------- */
    SET NOCOUNT ON
    SET XACT_ABORT ON

	-- Build Dynamic SQL to delete old records and execute it
	BEGIN TRY
		-- Example error checking to prevent deleting rows with a date within the last month
		-- IF @DeleteDate >= Dateadd(MONTH, - 1, sysdatetime())
		-- BEGIN
		--   RAISERROR ('Delete Date Too Recent - Delete cancelled',16,1);
        --     
		--	RETURN
		-- END

		-- Declare a variable to hold the dynamic SQL command
		DECLARE @Command NVARCHAR(4000)
		DECLARE @ParmDefinition NVARCHAR(4000) = '@SchemaName sysname, @TableName sysname, @ColumnName sysname, @RetentionDays int'
		DECLARE @DatabaseName NVARCHAR(4000) = DB_NAME()
		DECLARE @IndexName NVARCHAR(4000) = '' + quotename(@DatabaseName) + '.' + quotename(@SchemaName) + '.' + quotename(@TableName) + ''
		DECLARE @DeleteDate DATETIME = dateadd(DAY, -@RetentionDays, sysdatetime())

		-- Build the command by concatenating the input TableName and input DeleteDate
		SET @Command = 'DELETE TOP(' + convert(VARCHAR(10), @RowsToDelete) + ') FROM ' + quotename(@SchemaName) + '.' + quotename(@TableName) + ' WHERE ' + quotename(@ColumnName) + ' < ''' + convert(VARCHAR(20), @DeleteDate) + ''''
		
		-- Printing just to verify the syntax
		PRINT 'Command: ' + @command
		PRINT 'Database: ' + @DatabaseName
		PRINT 'Index: ' + @IndexName

		-- Dynamically execute the command we just built
		BEGIN TRAN
			EXECUTE sp_executesql 
				@Command,
				@ParmDefinition,
				@SchemaName = @SchemaName,
				@TableName = @TableName,
				@ColumnName = @ColumnName,
				@RetentionDays = @RetentionDays;
		
		PRINT Convert(Varchar(12),@@rowCount) + ' record(s) deleted from ' + quotename(@SchemaName) + '.' + quotename(@TableName) + ' table.';
        PRINT '=============================================================';
        PRINT ' ';
		COMMIT TRAN

	END TRY  

    BEGIN CATCH  
            ROLLBACK TRAN;
			PRINT N'Error Line = ' + CAST(ERROR_LINE() AS nvarchar(100));
            PRINT N'Error Message = ' + CAST(ERROR_MESSAGE() AS nvarchar(100));
    END CATCH

	-- Reorganize/Rebuild indexes 
	EXECUTE DBA.dbo.IndexOptimize
			@Databases = @DatabaseName,
			@FragmentationLow = NULL,
			@FragmentationMedium = 'INDEX_REORGANIZE,INDEX_REBUILD_ONLINE,INDEX_REBUILD_OFFLINE',
			@FragmentationHigh = 'INDEX_REBUILD_ONLINE,INDEX_REBUILD_OFFLINE',
			@FragmentationLevel1 = 5,
			@FragmentationLevel2 = 20,
			@Indexes = @IndexName;
	
END
GO
