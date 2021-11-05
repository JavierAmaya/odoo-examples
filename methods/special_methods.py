    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse() 
        if self.env.context.get('form_view_ref'):
            domain = [('is_expense', operator, 'True'),('name', operator, name)] + args
            recs = self.search(domain, limit=limit)
            return recs.name_get()
        else:
            domain = [('name', operator, name)] + args
            recs = self.search(domain, limit=limit)
            return recs.name_get()