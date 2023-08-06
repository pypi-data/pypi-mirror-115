#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 15:58:34 2021

@author: kevinmcbride
"""

  # Make simulation results go somewhere else - don't overwrite the existing results
    
    def _plot_all_Z_bounds(self):
        """Plot all concentration profiles
        
        """
        #%%
        # self = r1._plot_object
        # self.show = True
        # import numpy as np
        
        # fig = go.Figure()
        # use_spectral_format = False
        # pred = getattr(self.reaction_model.results, 'Z')
        # if hasattr(self.reaction_model.results, 'Cm'):
        #     exp = getattr(self.reaction_model.results, 'Cm')
        # elif hasattr(self.reaction_model.results, 'C'):
        #     if self.reaction_model.models['_s_model'] and not self.reaction_model.models['v_model'] and not self.reaction_model.models['p_model']:
        #         exp = None
        #     else:
        #         exp = getattr(self.reaction_model.results, 'C')
        #         use_spectral_format = True
        # else:
        #     exp = None
            
        # pred = self.reaction_model.results.Z
            
        # p_plus = {k: self.reaction_model.results_dict['p_estimator'].P[k] + self.reaction_model.results_dict['p_estimator'].deviations(0.99999)[k] for k in self.reaction_model.results_dict['p_estimator'].P.keys()}
        # self.reaction_model.simulate(parameters=p_plus)
        # pred_plus = self.reaction_model.results_dict['simulator'].Z
        
        # p_minus = {k: self.reaction_model.results_dict['p_estimator'].P[k] - self.reaction_model.results_dict['p_estimator'].deviations(0.99999)[k] for k in self.reaction_model.results_dict['p_estimator'].P.keys()}
        # self.reaction_model.simulate(parameters=p_minus)
        # pred_minus = self.reaction_model.results_dict['simulator'].Z

        # for i, col in enumerate(pred.columns):
            
        #     self._state_plot(fig, col, pred, exp, use_spectral_format=use_spectral_format)
            
        #     fig.add_trace(go.Scatter(
        #         x=np.concatenate([pred.index, pred.index[::-1]]),
        #         y=pd.concat([pred_plus[col], pred_minus[::-1][col]]),
        #         fill='toself',
        #         hoveron='points',
        #         opacity=0.2,
        #         fillcolor=colors[self.color_num],
        #         line=dict(color=colors[self.color_num], width=0),
        #     ))
        #     self.color_num += 1
        # # fig.show()
        # pio.write_html(fig, file='test', auto_open=True)    
        #%%
        
        # self.color_num = 0
        # var_data = self.reaction_model.components[col]
        # state = f'{self.reaction_model.components[col].state}'.capitalize()
        # title = f'Model: {self.reaction_model.name} | Concentration Profiles'
        # time_scale = f'Time [{self.reaction_model.unit_base.time}]'

        # state_units = self._get_proper_unit_str(var_data)
        # # state_units = var_data.units.u
        # fig.update_layout(
        #         title=title,
        #         xaxis_title=f'{time_scale}',
        #         yaxis_title=f'{state} [{state_units}]',
        #         )
        # self._fig_finishing(fig, pred, plot_name='all-concentration-profiles')

        #%%

        return None
    
#%%
