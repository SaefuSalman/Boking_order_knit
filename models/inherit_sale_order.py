from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking_order = fields.Boolean(string='Is Booking Order')
    service_team_id = fields.Many2one('service.team', string='Team', ondelete='cascade', required=True)
    team_leader_id = fields.Many2one('res.users', string='Team Leader', ondelete='cascade', required=True)
    team_member_ids = fields.Many2many('res.users', string='Team Members', required=True)
    booking_start = fields.Datetime(string='Booking Start', required=True)
    booking_end = fields.Datetime(string='Booking End', required=True)
    work_order_id = fields.Many2one('work.order', string='work order')

    @api.onchange('service_team_id')
    def _onchange_service_team_id(self):
        if self.service_team_id:
            self.team_leader_id = self.service_team_id.team_leader_id
            self.team_member_ids = self.service_team_id.team_member_ids.ids

    def check_team_availability(self):
        for order in self:
            overlapping_orders = self.env['work.order'].search([
                ('planned_start', '<', order.booking_end),
                ('planned_end', '>', order.booking_start),
                ('state', '=', 'cancel'),
                ('team_id', '=', order.service_team_id.id),
            ])
            if overlapping_orders:
                raise ValidationError(
                    _('Team already has work order during that period on %s') %
                    (order.display_name)
                )
            else:
                raise ValidationError(
                    _('Team is available for booking'))
                

    def action_confirm(self):
        overlapping_orders = self.env['work.order'].search([
                ('planned_start', '<', self.booking_end),
                ('planned_end', '>', self.booking_start),
                ('state', '=', 'cancel'),
                ('team_id', '=', self.service_team_id.id),
            ])
        res = super(SaleOrder, self).action_confirm()
        if overlapping_orders:
            raise ValidationError(
                    _('Team is not available during this period, already booked on. %s Please book on another date.') %
                    (self.display_name)
                )
        else:
            work_order = self.env['work.order'].create({
                'planned_start': self.booking_start,
                'planned_end': self.booking_end,
                'team_id': self.service_team_id.id,
                'team_leader_id': self.team_leader_id.id,
                'team_member_ids': [(6, 0, self.team_member_ids.ids)],
                'state': 'pending',
                'sale_order_id': self.id,
            })
            self.work_order_id = work_order.id

        return res

    def action_view_work_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Work Order',
            'res_model': 'work.order',
            'view_mode': 'form',
            'res_id': self.work_order_id.id,
        }