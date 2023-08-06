<?php
class ControllerExtensionJadeCustomfooterNewsletter extends Controller {
	private $error = array();

	public function index() {
		$this->load->language('extension/jade_customfooter_newsletter');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->load->model('extension/jade_customfooter_newsletter');

		$this->getList();
	}

	public function edit() {
		$this->load->language('extension/jade_customfooter_newsletter');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->load->model('extension/jade_customfooter_newsletter');

		if (($this->request->server['REQUEST_METHOD'] == 'POST') && $this->validateForm()) {
			$this->model_extension_jade_customfooter_newsletter->editJadeNewsletter($this->request->get['newsletter_id'], $this->request->post);

			$this->session->data['success'] = $this->language->get('text_success');

			$url = '';

			if (isset($this->request->get['sort'])) {
				$url .= '&sort=' . $this->request->get['sort'];
			}

			if (isset($this->request->get['order'])) {
				$url .= '&order=' . $this->request->get['order'];
			}

			if (isset($this->request->get['page'])) {
				$url .= '&page=' . $this->request->get['page'];
			}

			$this->response->redirect($this->url->link('extension/jade_customfooter_newsletter', 'user_token=' . $this->session->data['user_token'] . $url, true));
		}

		$this->getForm();
	}

	public function delete() {
		$this->load->language('extension/jade_customfooter_newsletter');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->load->model('extension/jade_customfooter_newsletter');

		if (isset($this->request->post['selected']) && $this->validateDelete()) {
			foreach ($this->request->post['selected'] as $newsletter_id) {
				$this->model_extension_jade_customfooter_newsletter->deleteJadeNewsletter($newsletter_id);
			}

			$this->session->data['success'] = $this->language->get('text_success');

			$url = '';

			if (isset($this->request->get['sort'])) {
				$url .= '&sort=' . $this->request->get['sort'];
			}

			if (isset($this->request->get['order'])) {
				$url .= '&order=' . $this->request->get['order'];
			}

			if (isset($this->request->get['page'])) {
				$url .= '&page=' . $this->request->get['page'];
			}

			$this->response->redirect($this->url->link('extension/jade_customfooter_newsletter', 'user_token=' . $this->session->data['user_token'] . $url, true));
		}

		$this->getList();
	}

	protected function getList() {
		if (isset($this->request->get['sort'])) {
			$sort = $this->request->get['sort'];
		} else {
			$sort = 'date_added';
		}

		if (isset($this->request->get['order'])) {
			$order = $this->request->get['order'];
		} else {
			$order = 'ASC';
		}

		if (isset($this->request->get['page'])) {
			$page = $this->request->get['page'];
		} else {
			$page = 1;
		}

		$url = '';

		if (isset($this->request->get['sort'])) {
			$url .= '&sort=' . $this->request->get['sort'];
		}

		if (isset($this->request->get['order'])) {
			$url .= '&order=' . $this->request->get['order'];
		}

		if (isset($this->request->get['page'])) {
			$url .= '&page=' . $this->request->get['page'];
		}

		$data['breadcrumbs'] = array();

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('text_home'),
			'href' => $this->url->link('common/dashboard', 'user_token=' . $this->session->data['user_token'], true)
		);

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('heading_title'),
			'href' => $this->url->link('extension/jade_customfooter_newsletter', 'user_token=' . $this->session->data['user_token'] . $url, true)
		);

		$data['send_email'] = $this->url->link('extension/jade_customfooter_newsletter/mail', 'user_token=' . $this->session->data['user_token'] . $url, true);
		$data['delete'] = $this->url->link('extension/jade_customfooter_newsletter/delete', 'user_token=' . $this->session->data['user_token'] . $url, true);

		$data['subscribers'] = array();

		$filter_data = array(
			'sort'  => $sort,
			'order' => $order,
			'start' => ($page - 1) * $this->config->get('config_limit_admin'),
			'limit' => $this->config->get('config_limit_admin')
		);

		$newsletter_total = $this->model_extension_jade_customfooter_newsletter->getTotalJadeNewsletters();

		$results = $this->model_extension_jade_customfooter_newsletter->getJadeNewsletters($filter_data);

		foreach ($results as $result) {
			$data['subscribers'][] = array(
				'newsletter_id' 	=> $result['newsletter_id'],
				'email'          	=> $result['email'],
				'status_number'		=> $result['status'],
				'status'     		=> $result['status'] ? $this->language->get('text_newsletter_verified') : $this->language->get('text_newsletter_unsubscriber'),
				'ip'          		=> $result['ip'],
				'date_added'     	=> date($this->language->get('date_format_short'), strtotime($result['date_added'])),
				'edit'           	=> $this->url->link('extension/jade_customfooter_newsletter/edit', 'user_token=' . $this->session->data['user_token'] . '&newsletter_id=' . $result['newsletter_id'] . $url, true)
			);
		}

		$data['heading_title'] = $this->language->get('heading_title');

		$data['text_list'] = $this->language->get('text_list');
		$data['text_no_results'] = $this->language->get('text_no_results');
		$data['text_confirm'] = $this->language->get('text_confirm');

		$data['column_email'] = $this->language->get('column_email');
		$data['column_status'] = $this->language->get('column_status');
		$data['column_action'] = $this->language->get('column_action');
		$data['column_ip'] = $this->language->get('column_ip');
		$data['column_date_added'] = $this->language->get('column_date_added');

		$data['button_send_email'] = $this->language->get('button_send_email');
		$data['button_edit'] = $this->language->get('button_edit');
		$data['button_delete'] = $this->language->get('button_delete');

		if (isset($this->error['warning'])) {
			$data['error_warning'] = $this->error['warning'];
		} else {
			$data['error_warning'] = '';
		}

		if (isset($this->session->data['success'])) {
			$data['success'] = $this->session->data['success'];

			unset($this->session->data['success']);
		} else {
			$data['success'] = '';
		}

		if (isset($this->request->post['selected'])) {
			$data['selected'] = (array)$this->request->post['selected'];
		} else {
			$data['selected'] = array();
		}

		$url = '';

		if ($order == 'ASC') {
			$url .= '&order=DESC';
		} else {
			$url .= '&order=ASC';
		}

		if (isset($this->request->get['page'])) {
			$url .= '&page=' . $this->request->get['page'];
		}

		$data['sort_email'] = $this->url->link('extension/jade_customfooter_newsletter', 'user_token=' . $this->session->data['user_token'] . '&sort=email' . $url, true);
		$data['sort_status'] = $this->url->link('extension/jade_customfooter_newsletter', 'user_token=' . $this->session->data['user_token'] . '&sort=status' . $url, true);
		$data['sort_ip'] = $this->url->link('extension/jade_customfooter_newsletter', 'user_token=' . $this->session->data['user_token'] . '&sort=ip' . $url, true);
		$data['sort_date_added'] = $this->url->link('extension/jade_customfooter_newsletter', 'user_token=' . $this->session->data['user_token'] . '&sort=date_added' . $url, true);

		$url = '';

		if (isset($this->request->get['sort'])) {
			$url .= '&sort=' . $this->request->get['sort'];
		}

		if (isset($this->request->get['order'])) {
			$url .= '&order=' . $this->request->get['order'];
		}

		$pagination = new Pagination();
		$pagination->total = $newsletter_total;
		$pagination->page = $page;
		$pagination->limit = $this->config->get('config_limit_admin');
		$pagination->url = $this->url->link('extension/jade_customfooter_newsletter', 'user_token=' . $this->session->data['user_token'] . $url . '&page={page}', true);

		$data['pagination'] = $pagination->render();

		$data['results'] = sprintf($this->language->get('text_pagination'), ($newsletter_total) ? (($page - 1) * $this->config->get('config_limit_admin')) + 1 : 0, ((($page - 1) * $this->config->get('config_limit_admin')) > ($newsletter_total - $this->config->get('config_limit_admin'))) ? $newsletter_total : ((($page - 1) * $this->config->get('config_limit_admin')) + $this->config->get('config_limit_admin')), $newsletter_total, ceil($newsletter_total / $this->config->get('config_limit_admin')));

		$data['sort'] = $sort;
		$data['order'] = $order;

		$data['header'] = $this->load->controller('common/header');
		$data['column_left'] = $this->load->controller('common/column_left');
		$data['footer'] = $this->load->controller('common/footer');

		$this->config->set('template_engine', 'template');
		$this->response->setOutput($this->load->view('extension/jade_customfooter_newsletter_list', $data));
	}

	protected function getForm() {
		$data['heading_title'] = $this->language->get('heading_title');

		$data['text_form'] = !isset($this->request->get['newsletter_id']) ? $this->language->get('text_add') : $this->language->get('text_edit');
		$data['text_default'] = $this->language->get('text_default');
		$data['text_enabled'] = $this->language->get('text_enabled');
		$data['text_disabled'] = $this->language->get('text_disabled');
		$data['text_newsletter_verified'] = $this->language->get('text_newsletter_verified');
		$data['text_newsletter_unsubscriber'] = $this->language->get('text_newsletter_unsubscriber');

		$data['entry_email'] = $this->language->get('entry_email');
		$data['entry_status'] = $this->language->get('entry_status');
		$data['entry_language'] = $this->language->get('entry_language');
		$data['entry_store'] = $this->language->get('entry_store');

		$data['button_save'] = $this->language->get('button_save');
		$data['button_cancel'] = $this->language->get('button_cancel');

		$data['tab_general'] = $this->language->get('tab_general');
		$data['tab_data'] = $this->language->get('tab_data');
		$data['tab_design'] = $this->language->get('tab_design');

		if (isset($this->error['warning'])) {
			$data['error_warning'] = $this->error['warning'];
		} else {
			$data['error_warning'] = '';
		}

		$url = '';

		if (isset($this->request->get['sort'])) {
			$url .= '&sort=' . $this->request->get['sort'];
		}

		if (isset($this->request->get['order'])) {
			$url .= '&order=' . $this->request->get['order'];
		}

		if (isset($this->request->get['page'])) {
			$url .= '&page=' . $this->request->get['page'];
		}

		$data['breadcrumbs'] = array();

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('text_home'),
			'href' => $this->url->link('common/dashboard', 'user_token=' . $this->session->data['user_token'], true)
		);

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('heading_title'),
			'href' => $this->url->link('extension/jade_customfooter_newsletter', 'user_token=' . $this->session->data['user_token'] . $url, true)
		);

		if (!isset($this->request->get['newsletter_id'])) {
			$data['action'] = $this->url->link('extension/jade_customfooter_newsletter/add', 'user_token=' . $this->session->data['user_token'] . $url, true);
		} else {
			$data['action'] = $this->url->link('extension/jade_customfooter_newsletter/edit', 'user_token=' . $this->session->data['user_token'] . '&newsletter_id=' . $this->request->get['newsletter_id'] . $url, true);
		}

		$data['cancel'] = $this->url->link('extension/jade_customfooter_newsletter', 'user_token=' . $this->session->data['user_token'] . $url, true);

		if (isset($this->request->get['newsletter_id']) && ($this->request->server['REQUEST_METHOD'] != 'POST')) {
			$newsletter_info = $this->model_extension_jade_customfooter_newsletter->getJadeNewsletter($this->request->get['newsletter_id']);
		}

		$data['user_token'] = $this->session->data['user_token'];


		if (isset($this->request->post['email'])) {
			$data['email'] = $this->request->post['email'];
		} elseif (!empty($newsletter_info)) {
			$data['email'] = $newsletter_info['email'];
		} else {
			$data['email'] = true;
		}

		if (isset($this->request->post['status'])) {
			$data['status'] = $this->request->post['status'];
		} elseif (!empty($newsletter_info)) {
			$data['status'] = $newsletter_info['status'];
		} else {
			$data['status'] = true;
		}

		if (isset($this->request->post['store_id'])) {
			$data['store_id'] = $this->request->post['store_id'];
		} elseif (!empty($newsletter_info)) {
			$data['store_id'] = $newsletter_info['store_id'];
		} else {
			$data['store_id'] = true;
		}

		if (isset($this->request->post['language_id'])) {
			$data['language_id'] = $this->request->post['language_id'];
		} elseif (!empty($newsletter_info)) {
			$data['language_id'] = $newsletter_info['language_id'];
		} else {
			$data['language_id'] = true;
		}

		$this->load->model('localisation/language');
		$data['languages'] = $this->model_localisation_language->getLanguages();

		// Stores
		$this->load->model('setting/store');

		$data['stores'] = array();

		$data['stores'][] = array(
			'store_id' => 0,
			'name'     => $this->language->get('text_default')
		);

		$results = $this->model_setting_store->getStores();

		foreach ($results as $result) {
			$data['stores'][] = array(
				'store_id' => $result['store_id'],
				'name'     => $result['name']
			);
		}

		$data['header'] = $this->load->controller('common/header');
		$data['column_left'] = $this->load->controller('common/column_left');
		$data['footer'] = $this->load->controller('common/footer');

		$this->config->set('template_engine', 'template');
		$this->response->setOutput($this->load->view('extension/jade_customfooter_newsletter_form', $data));
	}

	protected function validateForm() {
		if (!$this->user->hasPermission('modify', 'extension/jade_customfooter_newsletter')) {
			$this->error['warning'] = $this->language->get('error_permission');
		}

		if ($this->error && !isset($this->error['warning'])) {
			$this->error['warning'] = $this->language->get('error_warning');
		}

		return !$this->error;
	}

	protected function validateDelete() {
		if (!$this->user->hasPermission('modify', 'extension/jade_customfooter_newsletter')) {
			$this->error['warning'] = $this->language->get('error_permission');
		}

		return !$this->error;
	}

	public function mail() {
		$this->load->language('extension/jade_newsletter_mail');

		$this->document->setTitle($this->language->get('heading_title'));

		$data['heading_title'] = $this->language->get('heading_title');

		$data['text_default'] = $this->language->get('text_default');
		$data['text_newsletter'] = $this->language->get('text_newsletter');
		$data['text_loading'] = $this->language->get('text_loading');
		$data['text_newsletter'] = $this->language->get('text_newsletter');
		$data['text_newsletter_verified'] = $this->language->get('text_newsletter_verified');
		$data['text_newsletter_unsubscriber'] = $this->language->get('text_newsletter_unsubscriber');

		$data['entry_store'] = $this->language->get('entry_store');
		$data['entry_to'] = $this->language->get('entry_to');
		$data['entry_subject'] = $this->language->get('entry_subject');
		$data['entry_message'] = $this->language->get('entry_message');
		$data['entry_newsletters'] = $this->language->get('entry_newsletters');

		$data['help_newsletters'] = $this->language->get('help_newsletters');

		$data['button_send'] = $this->language->get('button_send');
		$data['button_cancel'] = $this->language->get('button_cancel');

		$data['user_token'] = $this->session->data['user_token'];

		$data['breadcrumbs'] = array();

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('text_home'),
			'href' => $this->url->link('common/dashboard', 'user_token=' . $this->session->data['user_token'], true)
		);

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('heading_newsletter'),
			'href' => $this->url->link('extension/jade_customfooter_newsletter', 'user_token=' . $this->session->data['user_token'], true)
		);

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('heading_title'),
			'href' => $this->url->link('extension/jade_customfooter_newsletter/mail', 'user_token=' . $this->session->data['user_token'], true)
		);

		$data['cancel'] = $this->url->link('extension/jade_customfooter_newsletter', 'user_token=' . $this->session->data['user_token'], true);

		$this->load->model('setting/store');
		$data['stores'] = $this->model_setting_store->getStores();

		$data['header'] = $this->load->controller('common/header');
		$data['column_left'] = $this->load->controller('common/column_left');
		$data['footer'] = $this->load->controller('common/footer');

		$this->config->set('template_engine', 'template');
		$this->response->setOutput($this->load->view('extension/jade_newsletter_mail', $data));
	}

	public function send() {
		$this->load->language('extension/jade_newsletter_mail');

		$json = array();

		if ($this->request->server['REQUEST_METHOD'] == 'POST') {
			if (!$this->user->hasPermission('modify', 'extension/jade_customfooter_newsletter')) {
				$json['error']['warning'] = $this->language->get('error_permission');
			}

			if (!$this->request->post['subject']) {
				$json['error']['subject'] = $this->language->get('error_subject');
			}

			if (!$this->request->post['message']) {
				$json['error']['message'] = $this->language->get('error_message');
			}

			if (!$json) {
				$this->load->model('setting/store');
				$store_info = $this->model_setting_store->getStore($this->request->post['store_id']);

				if ($store_info) {
					$store_name = $store_info['name'];
				} else {
					$store_name = $this->config->get('config_name');
				}

				$this->load->model('setting/setting');
				$setting = $this->model_setting_setting->getSetting('config', $this->request->post['store_id']);
				$store_email = isset($setting['config_email']) ? $setting['config_email'] : $this->config->get('config_email');

				$this->load->model('extension/jade_customfooter_newsletter');

				if (isset($this->request->get['page'])) {
					$page = $this->request->get['page'];
				} else {
					$page = 1;
				}

				$email_total = 0;

				$emails = array();

				switch ($this->request->post['to']) {
					case 'newsletter_verified':
						$newsletter_data = array(
							'filter_status' 	=> 1,
							'start'             => ($page - 1) * 10,
							'limit'             => 10
						);

						$email_total = $this->model_extension_jade_customfooter_newsletter->getTotalJadeNewsletters($newsletter_data);

						$results = $this->model_extension_jade_customfooter_newsletter->getJadeNewsletters($newsletter_data);

						foreach ($results as $result) {
							$emails[] = $result['email'];
						}
						break;
					case 'newsletter_unsubscriber':
						$newsletter_data = array(
							'filter_status' 	=> 0,
							'start'             => ($page - 1) * 10,
							'limit'             => 10
						);

						$email_total = $this->model_extension_jade_customfooter_newsletter->getTotalJadeNewsletters($newsletter_data);

						$results = $this->model_extension_jade_customfooter_newsletter->getJadeNewsletters($newsletter_data);

						foreach ($results as $result) {
							$emails[] = $result['email'];
						}
						break;
					case 'newsletters':
						if (!empty($this->request->post['newsletters'])) {
							foreach ($this->request->post['newsletters'] as $newsletter_id) {
								$newsleterr_info = $this->model_extension_jade_customfooter_newsletter->getJadeNewsletter($newsletter_id);

								if ($newsleterr_info) {
									$emails[] = $newsleterr_info['email'];
								}
							}
						}
						break;
				}

				if ($emails) {
					$json['success'] = $this->language->get('text_success');

					$start = ($page - 1) * 10;
					$end = $start + 10;

					if ($end < $email_total) {
						$json['success'] = sprintf($this->language->get('text_sent'), $start, $email_total);
					}

					if ($end < $email_total) {
						$json['next'] = str_replace('&amp;', '&', $this->url->link('extension/jade_customfooter_newsletter/send', 'user_token=' . $this->session->data['user_token'] . '&page=' . ($page + 1), true));
					} else {
						$json['next'] = '';
					}

					$message  = '<html dir="ltr" lang="en">' . "\n";
					$message .= '  <head>' . "\n";
					$message .= '    <title>' . $this->request->post['subject'] . '</title>' . "\n";
					$message .= '    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">' . "\n";
					$message .= '  </head>' . "\n";
					$message .= '  <body>' . html_entity_decode($this->request->post['message'], ENT_QUOTES, 'UTF-8') . '</body>' . "\n";
					$message .= '</html>' . "\n";

					foreach ($emails as $email) {
						if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
							if(VERSION >= '3.0.0.0') {
								$mail = new Mail($this->config->get('config_mail_engine'));
								$mail->parameter = $this->config->get('config_mail_parameter');
								$mail->smtp_hostname = $this->config->get('config_mail_smtp_hostname');
								$mail->smtp_username = $this->config->get('config_mail_smtp_username');
								$mail->smtp_password = html_entity_decode($this->config->get('config_mail_smtp_password'), ENT_QUOTES, 'UTF-8');
								$mail->smtp_port = $this->config->get('config_mail_smtp_port');
								$mail->smtp_timeout = $this->config->get('config_mail_smtp_timeout');
							} else if(VERSION <= '2.0.1.1') {
						     	$mail = new Mail($this->config->get('config_mail'));
						    } else {
								$mail = new Mail();
								$mail->protocol = $this->config->get('config_mail_protocol');
								$mail->parameter = $this->config->get('config_mail_parameter');
								$mail->smtp_hostname = $this->config->get('config_mail_smtp_hostname');
								$mail->smtp_username = $this->config->get('config_mail_smtp_username');
								$mail->smtp_password = html_entity_decode($this->config->get('config_mail_smtp_password'), ENT_QUOTES, 'UTF-8');
								$mail->smtp_port = $this->config->get('config_mail_smtp_port');
								$mail->smtp_timeout = $this->config->get('config_mail_smtp_timeout');
							}

							$mail->setTo($email);
							$mail->setFrom($store_email);
							$mail->setSender(html_entity_decode($store_name, ENT_QUOTES, 'UTF-8'));
							$mail->setSubject(html_entity_decode($this->request->post['subject'], ENT_QUOTES, 'UTF-8'));
							$mail->setHtml($message);
							$mail->send();
						}
					}
				} else {
					$json['error']['email'] = $this->language->get('error_email');
				}
			}
		}

		$this->response->addHeader('Content-Type: application/json');
		$this->response->setOutput(json_encode($json));
	}

	public function autocomplete() {
		$json = array();

		if (isset($this->request->get['filter_email'])) {
			if (isset($this->request->get['filter_email'])) {
				$filter_email = $this->request->get['filter_email'];
			} else {
				$filter_email = '';
			}

			$this->load->model('extension/jade_customfooter_newsletter');

			$filter_data = array(
				'filter_email' => $filter_email,
				'start'        => 0,
				'limit'        => 5
			);

			$results = $this->model_extension_jade_customfooter_newsletter->getJadeNewsletters($filter_data);

			foreach ($results as $result) {
				$json[] = array(
					'newsletter_id'       => $result['newsletter_id'],
					'email'           	  => $result['email'],
				);
			}
		}

		$sort_order = array();

		foreach ($json as $key => $value) {
			$sort_order[$key] = $value['email'];
		}

		array_multisort($sort_order, SORT_ASC, $json);

		$this->response->addHeader('Content-Type: application/json');
		$this->response->setOutput(json_encode($json));
	}
}