from odoo import models, fields, api, _

class WorkOrder(models.Model):
    _name = 'work.order'
    _description = 'Work Order'

    name = fields.Char(string='WO Number', required=True, readonly=True, default=lambda self: _('New'))
    sale_order_id = fields.Many2one('sale.order', string='Booking Order Reference', readonly=True)
    team_id = fields.Many2one('service.team', string='Team', required=True)
    team_leader_id = fields.Many2one('res.users', string='Team Leader', required=True)
    team_member_ids = fields.Many2many('res.users', string='Team Members')
    planned_start = fields.Datetime(string='Planned Start', required=True)
    planned_end = fields.Datetime(string='Planned End', required=True)
    date_start = fields.Datetime(string='Date Start', readonly=True)
    date_end = fields.Datetime(string='Date End', readonly=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='State', default='pending', track_visibility='onchange', readonly=True)
    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('work.order') or _('New')
        result = super(WorkOrder, self).create(vals)
        return result

    def action_start_work(self):
        self.ensure_one()
        self.write({
            'state': 'in_progress',
            'date_start': fields.Datetime.now(),
        })

    def action_end_work(self):
        self.ensure_one()
        self.write({
            'state': 'done',
            'date_end': fields.Datetime.now(),
        })

    def action_reset_work(self):
        self.ensure_one()
        self.write({
            'state': 'pending',
            'date_start': False,
        })

    def action_cancel_work(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'work.order.cancel.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_work_order_id': self.id}
        }

class WorkOrderCancelWizard(models.TransientModel):
    _name = 'work.order.cancel.wizard'
    _description = 'Work Order Cancel Wizard'

    work_order_id = fields.Many2one('work.order', required=True)
    reason = fields.Text('Reason for Cancellation', required=True)

    def confirm_cancellation(self):
        self.ensure_one()
        self.work_order_id.write({
            'state': 'cancelled',
            'notes': self.work_order_id.notes + '\nCancellation Reason: ' + self.reason if self.work_order_id.notes else 'Cancellation Reason: ' + self.reason
        })
