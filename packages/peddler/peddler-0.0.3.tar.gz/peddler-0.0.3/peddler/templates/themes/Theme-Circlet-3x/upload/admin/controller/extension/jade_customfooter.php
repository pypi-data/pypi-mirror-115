<?php
class ControllerExtensionJadeCustomfooter extends Controller {
	private $error = array();

	public function index() {
		$this->load->language('extension/jade_customfooter');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->load->model('extension/jade_customfooter');

		$this->getList();
	}

	public function add() {
		$this->load->language('extension/jade_customfooter');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->load->model('extension/jade_customfooter');

		if (($this->request->server['REQUEST_METHOD'] == 'POST') && $this->validateForm()) {
			$this->model_extension_jade_customfooter->addJadeCustomfooter($this->request->post);

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

			$this->response->redirect($this->url->link('extension/jade_customfooter', 'user_token=' . $this->session->data['user_token'] . $url, true));
		}

		$this->getForm();
	}

	public function edit() {
		$this->load->language('extension/jade_customfooter');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->load->model('extension/jade_customfooter');

		if (($this->request->server['REQUEST_METHOD'] == 'POST') && $this->validateForm()) {

			$this->model_extension_jade_customfooter->editJadeCustomfooter($this->request->get['jade_customfooter_id'], $this->request->post);

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

			$this->response->redirect($this->url->link('extension/jade_customfooter', 'user_token=' . $this->session->data['user_token'] . $url, true));
		}

		$this->getForm();
	}

	public function delete() {
		$this->load->language('extension/jade_customfooter');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->load->model('extension/jade_customfooter');

		if (isset($this->request->post['selected']) && $this->validateDelete()) {
			foreach ($this->request->post['selected'] as $jade_customfooter_id) {
				$this->model_extension_jade_customfooter->deleteJadeCustomfooter($jade_customfooter_id);
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

			$this->response->redirect($this->url->link('extension/jade_customfooter', 'user_token=' . $this->session->data['user_token'] . $url, true));
		}

		$this->getList();
	}

	protected function getList() {
		if (isset($this->request->get['sort'])) {
			$sort = $this->request->get['sort'];
		} else {
			$sort = 'jc.sort_order';
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
			'href' => $this->url->link('extension/jade_customfooter', 'user_token=' . $this->session->data['user_token'] . $url, true)
		);

		$data['add'] = $this->url->link('extension/jade_customfooter/add', 'user_token=' . $this->session->data['user_token'] . $url, true);
		$data['delete'] = $this->url->link('extension/jade_customfooter/delete', 'user_token=' . $this->session->data['user_token'] . $url, true);

		$data['jade_customfooters'] = array();

		$filter_data = array(
			'sort'  => $sort,
			'order' => $order,
			'start' => ($page - 1) * $this->config->get('config_limit_admin'),
			'limit' => $this->config->get('config_limit_admin')
		);

		$jade_customfooter_total = $this->model_extension_jade_customfooter->getTotalJadeCustomfooters();

		$results = $this->model_extension_jade_customfooter->getJadeCustomfooters($filter_data);

		foreach ($results as $result) {
			$data['jade_customfooters'][] = array(
				'jade_customfooter_id' => $result['jade_customfooter_id'],
				'title'          => $result['title'],
				'sort_order'     => $result['sort_order'],
				'edit'           => $this->url->link('extension/jade_customfooter/edit', 'user_token=' . $this->session->data['user_token'] . '&jade_customfooter_id=' . $result['jade_customfooter_id'] . $url, true)
			);
		}

		$data['heading_title'] = $this->language->get('heading_title');

		$data['text_list'] = $this->language->get('text_list');
		$data['text_no_results'] = $this->language->get('text_no_results');
		$data['text_confirm'] = $this->language->get('text_confirm');

		$data['column_title'] = $this->language->get('column_title');
		$data['column_sort_order'] = $this->language->get('column_sort_order');
		$data['column_action'] = $this->language->get('column_action');

		$data['button_add'] = $this->language->get('button_add');
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

		$data['sort_title'] = $this->url->link('extension/jade_customfooter', 'user_token=' . $this->session->data['user_token'] . '&sort=id.title' . $url, true);
		$data['sort_sort_order'] = $this->url->link('extension/jade_customfooter', 'user_token=' . $this->session->data['user_token'] . '&sort=i.sort_order' . $url, true);

		$url = '';

		if (isset($this->request->get['sort'])) {
			$url .= '&sort=' . $this->request->get['sort'];
		}

		if (isset($this->request->get['order'])) {
			$url .= '&order=' . $this->request->get['order'];
		}

		$pagination = new Pagination();
		$pagination->total = $jade_customfooter_total;
		$pagination->page = $page;
		$pagination->limit = $this->config->get('config_limit_admin');
		$pagination->url = $this->url->link('extension/jade_customfooter', 'user_token=' . $this->session->data['user_token'] . $url . '&page={page}', true);

		$data['pagination'] = $pagination->render();

		$data['results'] = sprintf($this->language->get('text_pagination'), ($jade_customfooter_total) ? (($page - 1) * $this->config->get('config_limit_admin')) + 1 : 0, ((($page - 1) * $this->config->get('config_limit_admin')) > ($jade_customfooter_total - $this->config->get('config_limit_admin'))) ? $jade_customfooter_total : ((($page - 1) * $this->config->get('config_limit_admin')) + $this->config->get('config_limit_admin')), $jade_customfooter_total, ceil($jade_customfooter_total / $this->config->get('config_limit_admin')));

		$data['sort'] = $sort;
		$data['order'] = $order;

		$data['header'] = $this->load->controller('common/header');
		$data['column_left'] = $this->load->controller('common/column_left');
		$data['footer'] = $this->load->controller('common/footer');

		$this->config->set('template_engine', 'template');
		$this->response->setOutput($this->load->view('extension/jade_customfooter_list', $data));
	}

	protected function getForm() {
		$data['heading_title'] = $this->language->get('heading_title');

		$data['text_form'] = !isset($this->request->get['jade_customfooter_id']) ? $this->language->get('text_add') : $this->language->get('text_edit');
		$data['text_default'] = $this->language->get('text_default');
		$data['text_enabled'] = $this->language->get('text_enabled');
		$data['text_disabled'] = $this->language->get('text_disabled');

		$data['entry_title'] = $this->language->get('entry_title');
		$data['entry_sort_order'] = $this->language->get('entry_sort_order');
		$data['entry_status'] = $this->language->get('entry_status');
		$data['entry_type'] = $this->language->get('entry_type');
		$data['entry_url'] = $this->language->get('entry_url');
		$data['entry_icon'] = $this->language->get('entry_icon');
		$data['entry_image'] = $this->language->get('entry_image');
		$data['entry_description'] = $this->language->get('entry_description');
		$data['entry_placeholder'] = $this->language->get('entry_placeholder');
		$data['entry_button_text'] = $this->language->get('entry_button_text');
		$data['entry_action'] = $this->language->get('entry_action');
		$data['entry_hotline_title'] = $this->language->get('entry_hotline_title');
		$data['entry_hotline_description'] = $this->language->get('entry_hotline_description');
		$data['entry_size_class'] = $this->language->get('entry_size_class');
		$data['entry_customer_group'] = $this->language->get('entry_customer_group');
		$data['entry_store'] = $this->language->get('entry_store');

		$data['button_contactdetail_add'] = $this->language->get('button_contactdetail_add');
		$data['button_accountlinks_add'] = $this->language->get('button_accountlinks_add');
		$data['button_informationlinks_add'] = $this->language->get('button_informationlinks_add');
		$data['button_sociallinks_add'] = $this->language->get('button_sociallinks_add');
		$data['button_payments_add'] = $this->language->get('button_payments_add');
		$data['button_appicons_add'] = $this->language->get('button_appicons_add');
		$data['button_remove'] = $this->language->get('button_remove');
		$data['button_save'] = $this->language->get('button_save');
		$data['button_cancel'] = $this->language->get('button_cancel');

		$data['tab_general'] = $this->language->get('tab_general');
		$data['tab_data'] = $this->language->get('tab_data');
		$data['tab_link'] = $this->language->get('tab_link');

		$data['type_contact_detail'] = $this->language->get('type_contact_detail');
		$data['type_newsletter'] = $this->language->get('type_newsletter');
		$data['type_account_links'] = $this->language->get('type_account_links');
		$data['type_social_icons'] = $this->language->get('type_social_icons');
		$data['type_information_links'] = $this->language->get('type_information_links');
		$data['type_payments_icons'] = $this->language->get('type_payments_icons');
		$data['type_app_icons'] = $this->language->get('type_app_icons');
		$data['type_editor'] = $this->language->get('type_editor');
		$data['type_hotline'] = $this->language->get('type_hotline');

		if (isset($this->error['warning'])) {
			$data['error_warning'] = $this->error['warning'];
		} else {
			$data['error_warning'] = '';
		}

		if (isset($this->error['title'])) {
			$data['error_title'] = $this->error['title'];
		} else {
			$data['error_title'] = array();
		}

		if (isset($this->error['contactdetail'])) {
			$data['error_contactdetail'] = $this->error['contactdetail'];
		} else {
			$data['error_contactdetail'] = array();
		}

		if (isset($this->error['accountlinks'])) {
			$data['error_accountlinks'] = $this->error['accountlinks'];
		} else {
			$data['error_accountlinks'] = array();
		}

		if (isset($this->error['informationlinks'])) {
			$data['error_informationlinks'] = $this->error['informationlinks'];
		} else {
			$data['error_informationlinks'] = array();
		}

		if (isset($this->error['sociallinks'])) {
			$data['error_sociallinks'] = $this->error['sociallinks'];
		} else {
			$data['error_sociallinks'] = array();
		}

		if (isset($this->error['payments'])) {
			$data['error_payments'] = $this->error['payments'];
		} else {
			$data['error_payments'] = array();
		}

		if (isset($this->error['appicons'])) {
			$data['error_appicons'] = $this->error['appicons'];
		} else {
			$data['error_appicons'] = array();
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
			'href' => $this->url->link('extension/jade_customfooter', 'user_token=' . $this->session->data['user_token'] . $url, true)
		);

		if (!isset($this->request->get['jade_customfooter_id'])) {
			$data['action'] = $this->url->link('extension/jade_customfooter/add', 'user_token=' . $this->session->data['user_token'] . $url, true);
		} else {
			$data['action'] = $this->url->link('extension/jade_customfooter/edit', 'user_token=' . $this->session->data['user_token'] . '&jade_customfooter_id=' . $this->request->get['jade_customfooter_id'] . $url, true);
		}

		$data['cancel'] = $this->url->link('extension/jade_customfooter', 'user_token=' . $this->session->data['user_token'] . $url, true);

		if (isset($this->request->get['jade_customfooter_id']) && ($this->request->server['REQUEST_METHOD'] != 'POST')) {
			$jade_customfooter_info = $this->model_extension_jade_customfooter->getJadeCustomfooter($this->request->get['jade_customfooter_id']);
		}

		$data['user_token'] = $this->session->data['user_token'];

		$this->load->model('localisation/language');

		$data['languages'] = $this->model_localisation_language->getLanguages();

		if (isset($this->request->post['jade_customfooter_description'])) {
			$data['jade_customfooter_description'] = $this->request->post['jade_customfooter_description'];
		} elseif (isset($this->request->get['jade_customfooter_id'])) {
			$data['jade_customfooter_description'] = $this->model_extension_jade_customfooter->getJadeCustomfooterDescriptions($this->request->get['jade_customfooter_id']);
		} else {
			$data['jade_customfooter_description'] = array();
		}

		if (isset($this->request->post['status'])) {
			$data['status'] = $this->request->post['status'];
		} elseif (!empty($jade_customfooter_info)) {
			$data['status'] = $jade_customfooter_info['status'];
		} else {
			$data['status'] = true;
		}

		if (isset($this->request->post['type_code'])) {
			$data['type_code'] = $this->request->post['type_code'];
		} elseif (!empty($jade_customfooter_info)) {
			$data['type_code'] = $jade_customfooter_info['type_code'];
		} else {
			$data['type_code'] = 'contact_detail';
		}

		if (isset($this->request->post['size_class'])) {
			$data['size_class'] = $this->request->post['size_class'];
		} elseif (!empty($jade_customfooter_info)) {
			$data['size_class'] = $jade_customfooter_info['size_class'];
		} else {
			$data['size_class'] = '';
		}

		if (isset($this->request->post['sort_order'])) {
			$data['sort_order'] = $this->request->post['sort_order'];
		} elseif (!empty($jade_customfooter_info)) {
			$data['sort_order'] = $jade_customfooter_info['sort_order'];
		} else {
			$data['sort_order'] = '';
		}

		if (isset($this->request->post['contactdetail_table'])) {
			$data['contactdetail_tables'] = $this->request->post['contactdetail_table'];
		} elseif (!empty($jade_customfooter_info['contactdetail_table'])) {
			$data['contactdetail_tables'] = json_decode($jade_customfooter_info['contactdetail_table'], 1);
		} else {
			$data['contactdetail_tables'] = array();
		}

		if (isset($this->request->post['accountlinks_table'])) {
			$data['accountlinks_tables'] = $this->request->post['accountlinks_table'];
		} elseif (!empty($jade_customfooter_info['accountlinks_table'])) {
			$data['accountlinks_tables'] = json_decode($jade_customfooter_info['accountlinks_table'], 1);
		} else {
			$data['accountlinks_tables'] = array();
		}

		if (isset($this->request->post['informationlinks_table'])) {
			$data['informationlinks_tables'] = $this->request->post['informationlinks_table'];
		} elseif (!empty($jade_customfooter_info['informationlinks_table'])) {
			$data['informationlinks_tables'] = json_decode($jade_customfooter_info['informationlinks_table'], 1);
		} else {
			$data['informationlinks_tables'] = array();
		}

		if (isset($this->request->post['sociallinks_table'])) {
			$data['sociallinks_tables'] = $this->request->post['sociallinks_table'];
		} elseif (!empty($jade_customfooter_info['sociallinks_table'])) {
			$data['sociallinks_tables'] = json_decode($jade_customfooter_info['sociallinks_table'], 1);
		} else {
			$data['sociallinks_tables'] = array();
		}

		if (isset($this->request->post['payments_table'])) {
			$payments_tables = $this->request->post['payments_table'];
		} elseif (!empty($jade_customfooter_info['payments_table'])) {
			$payments_tables = json_decode($jade_customfooter_info['payments_table'], 1);
		} else {
			$payments_tables = array();
		}

		$this->load->model('tool/image');

		$data['payments_tables'] = array();
		foreach ($payments_tables as $key => $payments_table) {
			if (!empty($payments_table['image']) && is_file(DIR_IMAGE . $payments_table['image'])) {
				$payment_thumb = $this->model_tool_image->resize($payments_table['image'], 100, 100);
			} else {
				$payment_thumb = $this->model_tool_image->resize('no_image.png', 100, 100);
			}

			$data['payments_tables'][] = array(
				'payments_description'		=> isset($payments_table['payments_description']) ? $payments_table['payments_description'] : array(),
				'image'						=> isset($payments_table['image']) ? $payments_table['image'] : '',
				'thumb'						=> $payment_thumb,
			);
		}

		if (isset($this->request->post['appicons_table'])) {
			$appicons_tables = $this->request->post['appicons_table'];
		} elseif (!empty($jade_customfooter_info['appicons_table'])) {
			$appicons_tables = json_decode($jade_customfooter_info['appicons_table'], 1);
		} else {
			$appicons_tables = array();
		}

		$this->load->model('tool/image');

		$data['appicons_tables'] = array();
		foreach ($appicons_tables as $key => $appicons_table) {
			if (!empty($appicons_table['image']) && is_file(DIR_IMAGE . $appicons_table['image'])) {
				$appicons_thumb = $this->model_tool_image->resize($appicons_table['image'], 100, 100);
			} else {
				$appicons_thumb = $this->model_tool_image->resize('no_image.png', 100, 100);
			}

			$data['appicons_tables'][] = array(
				'appicons_description'		=> isset($appicons_table['appicons_description']) ? $appicons_table['appicons_description'] : array(),
				'image'						=> isset($appicons_table['image']) ? $appicons_table['image'] : '',
				'thumb'						=> $appicons_thumb,
			);
		}


		if (isset($this->request->post['editor_description'])) {
			$data['editor_description'] = $this->request->post['editor_description'];
		} elseif (!empty($jade_customfooter_info['editor_description'])) {
			$data['editor_description'] = json_decode($jade_customfooter_info['editor_description'], 1);
		} else {
			$data['editor_description'] = array();
		}

		if (isset($this->request->post['newsletter_table'])) {
			$data['newsletter_table'] = $this->request->post['newsletter_table'];
		} elseif (!empty($jade_customfooter_info['newsletter_table'])) {
			$data['newsletter_table'] = json_decode($jade_customfooter_info['newsletter_table'], 1);
		} else {
			$data['newsletter_table'] = array();
		}

		$this->load->model('setting/store');
		$data['stores'] = $this->model_setting_store->getStores();

		$this->load->model('customer/customer_group');
		$data['customer_groups'] = $this->model_customer_customer_group->getCustomerGroups();

		if (isset($this->request->post['jade_customfooter_customer_group'])) {
			$data['jade_customfooter_customer_group'] = $this->request->post['jade_customfooter_customer_group'];
		} elseif (isset($this->request->get['jade_customfooter_id'])) {
			$data['jade_customfooter_customer_group'] = $this->model_extension_jade_customfooter->getFooterCustomerGroups($this->request->get['jade_customfooter_id']);
		} else {
			$data['jade_customfooter_customer_group'] = array($this->config->get('config_customer_group_id'));
		}

		if (isset($this->request->post['jade_customfooter_store'])) {
			$data['jade_customfooter_store'] = $this->request->post['jade_customfooter_store'];
		} elseif (isset($this->request->get['jade_customfooter_id'])) {
			$data['jade_customfooter_store'] = $this->model_extension_jade_customfooter->getFooterStores($this->request->get['jade_customfooter_id']);
		} else {
			$data['jade_customfooter_store'] = array(0);
		}

		$data['placeholder'] = $this->model_tool_image->resize('no_image.png', 100, 100);

		$data['types'] = array();
		$data['types'][] = array(
			'code'		=> 'contact_detail',
			'title'		=> $this->language->get('type_contact_detail'),
		);
		$data['types'][] = array(
			'code'		=> 'newsletter',
			'title'		=> $this->language->get('type_newsletter'),
		);
		$data['types'][] = array(
			'code'		=> 'account_links',
			'title'		=> $this->language->get('type_account_links'),
		);
		$data['types'][] = array(
			'code'		=> 'information_links',
			'title'		=> $this->language->get('type_information_links'),
		);
		$data['types'][] = array(
			'code'		=> 'social_icons',
			'title'		=> $this->language->get('type_social_icons'),
		);
		$data['types'][] = array(
			'code'		=> 'payments_icons',
			'title'		=> $this->language->get('type_payments_icons'),
		);
		$data['types'][] = array(
			'code'		=> 'app_icons',
			'title'		=> $this->language->get('type_app_icons'),
		);
		$data['types'][] = array(
			'code'		=> 'editor',
			'title'		=> $this->language->get('type_editor'),
		);


		// Size Classes
		$data['size_classes'] = array();
		$data['size_classes'][] = array(
			'code'		=> 'j-sm-1',
			'title'		=> $this->language->get('text_size_1'),
		);

		$data['size_classes'][] = array(
			'code'		=> 'j-sm-2',
			'title'		=> $this->language->get('text_size_2'),
		);

		$data['size_classes'][] = array(
			'code'		=> 'j-sm-3',
			'title'		=> $this->language->get('text_size_3'),
		);

		$data['size_classes'][] = array(
			'code'		=> 'j-sm-4',
			'title'		=> $this->language->get('text_size_4'),
		);

		$data['size_classes'][] = array(
			'code'		=> 'j-sm-5',
			'title'		=> $this->language->get('text_size_5'),
		);

		$data['size_classes'][] = array(
			'code'		=> 'j-sm-6',
			'title'		=> $this->language->get('text_size_6'),
		);

		$data['size_classes'][] = array(
			'code'		=> 'j-sm-7',
			'title'		=> $this->language->get('text_size_7'),
		);

		$data['size_classes'][] = array(
			'code'		=> 'j-sm-8',
			'title'		=> $this->language->get('text_size_8'),
		);

		$data['size_classes'][] = array(
			'code'		=> 'j-sm-9',
			'title'		=> $this->language->get('text_size_9'),
		);

		$data['size_classes'][] = array(
			'code'		=> 'j-sm-10',
			'title'		=> $this->language->get('text_size_10'),
		);

		$data['size_classes'][] = array(
			'code'		=> 'j-sm-11',
			'title'		=> $this->language->get('text_size_11'),
		);

		$data['size_classes'][] = array(
			'code'		=> 'j-sm-12',
			'title'		=> $this->language->get('text_size_12'),
		);

		$data['header'] = $this->load->controller('common/header');
		$data['column_left'] = $this->load->controller('common/column_left');
		$data['footer'] = $this->load->controller('common/footer');

		$this->config->set('template_engine', 'template');
		$this->response->setOutput($this->load->view('extension/jade_customfooter_form', $data));
	}

	protected function validateForm() {
		if (!$this->user->hasPermission('modify', 'extension/jade_customfooter')) {
			$this->error['warning'] = $this->language->get('error_permission');
		}

		foreach ($this->request->post['jade_customfooter_description'] as $language_id => $value) {
			if ((utf8_strlen($value['title']) < 3) || (utf8_strlen($value['title']) > 64)) {
				$this->error['title'][$language_id] = $this->language->get('error_title');
			}
		}

		if (isset($this->request->post['contactdetail_table'])) {
			foreach ($this->request->post['contactdetail_table'] as $contactdetail_row => $contactdetail_table) {
				foreach ($contactdetail_table['contactdetail_description'] as $language_id => $contactdetail_description) {
					if (utf8_strlen($contactdetail_description['title']) < 3) {
						$this->error['contactdetail'][$contactdetail_row][$language_id] = $this->language->get('error_row_title');
					}
				}
			}
		}

		if (isset($this->request->post['accountlinks_table'])) {
			foreach ($this->request->post['accountlinks_table'] as $accountlinks_row => $accountlinks_table) {
				foreach ($accountlinks_table['accountlinks_description'] as $language_id => $accountlinks_description) {
					if (utf8_strlen($accountlinks_description['title']) < 3) {
						$this->error['accountlinks'][$accountlinks_row][$language_id] = $this->language->get('error_row_title');
					}
				}
			}
		}

		if (isset($this->request->post['informationlinks_table'])) {
			foreach ($this->request->post['informationlinks_table'] as $informationlinks_row => $informationlinks_table) {
				foreach ($informationlinks_table['informationlinks_description'] as $language_id => $informationlinks_description) {
					if (utf8_strlen($informationlinks_description['title']) < 3) {
						$this->error['informationlinks'][$informationlinks_row][$language_id] = $this->language->get('error_row_title');
					}
				}
			}
		}

		if (isset($this->request->post['sociallinks_table'])) {
			foreach ($this->request->post['sociallinks_table'] as $sociallinks_row => $sociallinks_table) {
				foreach ($sociallinks_table['sociallinks_description'] as $language_id => $sociallinks_description) {
					if (utf8_strlen($sociallinks_description['title']) < 3) {
						$this->error['sociallinks'][$sociallinks_row][$language_id] = $this->language->get('error_row_title');
					}
				}
			}
		}

		if (isset($this->request->post['payments_table'])) {
			foreach ($this->request->post['payments_table'] as $payments_row => $payments_table) {
				foreach ($payments_table['payments_description'] as $language_id => $payments_description) {
					if (utf8_strlen($payments_description['title']) < 3) {
						$this->error['payments'][$payments_row][$language_id] = $this->language->get('error_row_title');
					}
				}
			}
		}

		if (isset($this->request->post['appicons_table'])) {
			foreach ($this->request->post['appicons_table'] as $appicons_row => $appicons_table) {
				foreach ($appicons_table['appicons_description'] as $language_id => $appicons_description) {
					if (utf8_strlen($appicons_description['title']) < 3) {
						$this->error['appicons'][$appicons_row][$language_id] = $this->language->get('error_row_title');
					}
				}
			}
		}

		if ($this->error && !isset($this->error['warning'])) {
			$this->error['warning'] = $this->language->get('error_warning');
		}

		return !$this->error;
	}

	protected function validateDelete() {
		if (!$this->user->hasPermission('modify', 'extension/jade_customfooter')) {
			$this->error['warning'] = $this->language->get('error_permission');
		}

		return !$this->error;
	}
}