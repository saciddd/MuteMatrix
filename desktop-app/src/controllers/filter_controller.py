class FilterController:
    def __init__(self, table_view):
        self.table_view = table_view

    def apply_filter(self, filter_criteria):
        filtered_data = self.table_view.data
        
        if filter_criteria.get("tc_no"):
            filtered_data = [row for row in filtered_data if row['tc_no'] == filter_criteria["tc_no"]]
        
        if filter_criteria.get("name"):
            filtered_data = [row for row in filtered_data if filter_criteria["name"].lower() in row['name'].lower()]
        
        if filter_criteria.get("date"):
            filtered_data = [row for row in filtered_data if row['date'] == filter_criteria["date"]]
        
        if filter_criteria.get("operation_type"):
            filtered_data = [row for row in filtered_data if row['operation_type'] == filter_criteria["operation_type"]]
        
        self.table_view.update_displayed_data(filtered_data)

    def clear_filter(self):
        self.table_view.update_displayed_data(self.table_view.data)