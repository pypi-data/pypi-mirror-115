<?php
class ControllerCatalogJadetestimonial extends Controller {
	private $error = array();

	public function index() {
		$this->load->language('catalog/jade_testimonial');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->load->model('catalog/jade_testimonial');

		$this->load->model('tool/image');

		$this->model_catalog_jade_testimonial->create__Jade__Testimonial__Tables();

		$this->getList();
	}

	public function add() {
		$this->load->language('catalog/jade_testimonial');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->load->model('catalog/jade_testimonial');

		if (($this->request->server['REQUEST_METHOD'] == 'POST') && $this->validateForm()) {
			$this->model_catalog_jade_testimonial->addJadeTestimonial($this->request->post);

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

			$this->response->redirect($this->url->link('catalog/jade_testimonial', 'user_token=' . $this->session->data['user_token'] . $url, true));
		}

		$this->getForm();
	}

	public function edit() {
		$this->load->language('catalog/jade_testimonial');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->load->model('catalog/jade_testimonial');

		if (($this->request->server['REQUEST_METHOD'] == 'POST') && $this->validateForm()) {
			$this->model_catalog_jade_testimonial->editJadeTestimonial($this->request->get['jade_testimonial_id'], $this->request->post);

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

			$this->response->redirect($this->url->link('catalog/jade_testimonial', 'user_token=' . $this->session->data['user_token'] . $url, true));
		}

		$this->getForm();
	}

	public function delete() {
		$this->load->language('catalog/jade_testimonial');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->load->model('catalog/jade_testimonial');

		$this->load->model('tool/image');

		if (isset($this->request->post['selected']) && $this->validateDelete()) {
			foreach ($this->request->post['selected'] as $jade_testimonial_id) {
				$this->model_catalog_jade_testimonial->deleteJadeTestimonial($jade_testimonial_id);
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

			$this->response->redirect($this->url->link('catalog/jade_testimonial', 'user_token=' . $this->session->data['user_token'] . $url, true));
		}

		$this->getList();
	}

	protected function getList() {
		if (isset($this->request->get['sort'])) {
			$sort = $this->request->get['sort'];
		} else {
			$sort = 'td.title';
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
			'href' => $this->url->link('catalog/jade_testimonial', 'user_token=' . $this->session->data['user_token'] . $url, true)
		);

		$data['add'] = $this->url->link('catalog/jade_testimonial/add', 'user_token=' . $this->session->data['user_token'] . $url, true);
		$data['delete'] = $this->url->link('catalog/jade_testimonial/delete', 'user_token=' . $this->session->data['user_token'] . $url, true);

		$data['jade_testimonials'] = array();

		$filter_data = array(
			'sort'  => $sort,
			'order' => $order,
			'start' => ($page - 1) * $this->config->get('config_limit_admin'),
			'limit' => $this->config->get('config_limit_admin')
		);

		$jade_testimonial_total = $this->model_catalog_jade_testimonial->getTotalJadeTestimonials();

		$results = $this->model_catalog_jade_testimonial->getJadeTestimonials($filter_data);

		foreach ($results as $result) {
			if (is_file(DIR_IMAGE . $result['image'])) {
				$image = $this->model_tool_image->resize($result['image'], 100, 100);
			} else {
				$image = $this->model_tool_image->resize('nouserpic.png', 100, 100);
			}

			$data['jade_testimonials'][] = array(
				'jade_testimonial_id' => $result['jade_testimonial_id'],
				'title'          => $result['title'],
				'author'         => $result['author'],
				'destination'    => $result['destination'],
				'rating'         => $result['rating'],
				'image'      	 => $image,
				'sort_order'     => $result['sort_order'],
				'status'     => $result['status'] ? $this->language->get('text_enabled') : $this->language->get('text_disabled'),
				'edit'           => $this->url->link('catalog/jade_testimonial/edit', 'user_token=' . $this->session->data['user_token'] . '&jade_testimonial_id=' . $result['jade_testimonial_id'] . $url, true)
			);
		}

		$data['heading_title'] = $this->language->get('heading_title');

		$data['text_list'] = $this->language->get('text_list');
		$data['text_no_results'] = $this->language->get('text_no_results');
		$data['text_confirm'] = $this->language->get('text_confirm');

		$data['column_image'] = $this->language->get('column_image');
		$data['column_author'] = $this->language->get('column_author');
		$data['column_destination'] = $this->language->get('column_destination');
		$data['column_title'] = $this->language->get('column_title');
		$data['column_sort_order'] = $this->language->get('column_sort_order');
		$data['column_rating'] = $this->language->get('column_rating');
		$data['column_status'] = $this->language->get('column_status');
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

		$data['sort_title'] = $this->url->link('catalog/jade_testimonial', 'user_token=' . $this->session->data['user_token'] . '&sort=td.title' . $url, true);
		$data['sort_sort_order'] = $this->url->link('catalog/jade_testimonial', 'user_token=' . $this->session->data['user_token'] . '&sort=t.sort_order' . $url, true);
		$data['sort_rating'] = $this->url->link('catalog/jade_testimonial', 'user_token=' . $this->session->data['user_token'] . '&sort=t.rating' . $url, true);
		$data['sort_status'] = $this->url->link('catalog/jade_testimonial', 'user_token=' . $this->session->data['user_token'] . '&sort=t.status' . $url, true);
		$data['sort_author'] = $this->url->link('catalog/jade_testimonial', 'user_token=' . $this->session->data['user_token'] . '&sort=t.author' . $url, true);
		$data['sort_destination'] = $this->url->link('catalog/jade_testimonial', 'user_token=' . $this->session->data['user_token'] . '&sort=td.destination' . $url, true);

		$url = '';

		if (isset($this->request->get['sort'])) {
			$url .= '&sort=' . $this->request->get['sort'];
		}

		if (isset($this->request->get['order'])) {
			$url .= '&order=' . $this->request->get['order'];
		}

		$pagination = new Pagination();
		$pagination->total = $jade_testimonial_total;
		$pagination->page = $page;
		$pagination->limit = $this->config->get('config_limit_admin');
		$pagination->url = $this->url->link('catalog/jade_testimonial', 'user_token=' . $this->session->data['user_token'] . $url . '&page={page}', true);

		$data['pagination'] = $pagination->render();

		$data['results'] = sprintf($this->language->get('text_pagination'), ($jade_testimonial_total) ? (($page - 1) * $this->config->get('config_limit_admin')) + 1 : 0, ((($page - 1) * $this->config->get('config_limit_admin')) > ($jade_testimonial_total - $this->config->get('config_limit_admin'))) ? $jade_testimonial_total : ((($page - 1) * $this->config->get('config_limit_admin')) + $this->config->get('config_limit_admin')), $jade_testimonial_total, ceil($jade_testimonial_total / $this->config->get('config_limit_admin')));

		$data['sort'] = $sort;
		$data['order'] = $order;

		$data['header'] = $this->load->controller('common/header');
		$data['column_left'] = $this->load->controller('common/column_left');
		$data['footer'] = $this->load->controller('common/footer');

		$this->config->set('template_engine', 'template');
		$this->response->setOutput($this->load->view('catalog/jade_testimonial_list', $data));
	}

	protected function getForm() {
		$data['heading_title'] = $this->language->get('heading_title');

		$data['text_form'] = !isset($this->request->get['jade_testimonial_id']) ? $this->language->get('text_add') : $this->language->get('text_edit');
		$data['text_default'] = $this->language->get('text_default');
		$data['text_enabled'] = $this->language->get('text_enabled');
		$data['text_disabled'] = $this->language->get('text_disabled');
		$data['text_star'] = $this->language->get('text_star');

		$data['entry_title'] = $this->language->get('entry_title');
		$data['entry_description'] = $this->language->get('entry_description');
		$data['entry_destination'] = $this->language->get('entry_destination');
		$data['entry_author'] = $this->language->get('entry_author');
		$data['entry_rating'] = $this->language->get('entry_rating');
		$data['entry_image'] = $this->language->get('entry_image');
		$data['entry_sort_order'] = $this->language->get('entry_sort_order');
		$data['entry_status'] = $this->language->get('entry_status');

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

		if (isset($this->error['title'])) {
			$data['error_title'] = $this->error['title'];
		} else {
			$data['error_title'] = array();
		}

		if (isset($this->error['destination'])) {
			$data['error_destination'] = $this->error['destination'];
		} else {
			$data['error_destination'] = array();
		}

		if (isset($this->error['author'])) {
			$data['error_author'] = $this->error['author'];
		} else {
			$data['error_author'] = '';
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
			'href' => $this->url->link('catalog/jade_testimonial', 'user_token=' . $this->session->data['user_token'] . $url, true)
		);

		if (!isset($this->request->get['jade_testimonial_id'])) {
			$data['action'] = $this->url->link('catalog/jade_testimonial/add', 'user_token=' . $this->session->data['user_token'] . $url, true);
		} else {
			$data['action'] = $this->url->link('catalog/jade_testimonial/edit', 'user_token=' . $this->session->data['user_token'] . '&jade_testimonial_id=' . $this->request->get['jade_testimonial_id'] . $url, true);
		}

		$data['cancel'] = $this->url->link('catalog/jade_testimonial', 'user_token=' . $this->session->data['user_token'] . $url, true);

		if (isset($this->request->get['jade_testimonial_id']) && ($this->request->server['REQUEST_METHOD'] != 'POST')) {
			$jade_testimonial_info = $this->model_catalog_jade_testimonial->getJadeTestimonial($this->request->get['jade_testimonial_id']);
		}

		if (isset($this->request->post['jade_testimonial_description'])) {
			$data['jade_testimonial_description'] = $this->request->post['jade_testimonial_description'];
		} elseif (isset($this->request->get['jade_testimonial_id'])) {
			$data['jade_testimonial_description'] = $this->model_catalog_jade_testimonial->getJadeTestimonialDescriptions($this->request->get['jade_testimonial_id']);
		} else {
			$data['jade_testimonial_description'] = array();
		}

		if (isset($this->request->post['status'])) {
			$data['status'] = $this->request->post['status'];
		} elseif (!empty($jade_testimonial_info)) {
			$data['status'] = $jade_testimonial_info['status'];
		} else {
			$data['status'] = true;
		}

		if (isset($this->request->post['sort_order'])) {
			$data['sort_order'] = $this->request->post['sort_order'];
		} elseif (!empty($jade_testimonial_info)) {
			$data['sort_order'] = $jade_testimonial_info['sort_order'];
		} else {
			$data['sort_order'] = '';
		}

		if (isset($this->request->post['author'])) {
			$data['author'] = $this->request->post['author'];
		} elseif (!empty($jade_testimonial_info)) {
			$data['author'] = $jade_testimonial_info['author'];
		} else {
			$data['author'] = '';
		}

		if (isset($this->request->post['rating'])) {
			$data['rating'] = $this->request->post['rating'];
		} elseif (!empty($jade_testimonial_info)) {
			$data['rating'] = $jade_testimonial_info['rating'];
		} else {
			$data['rating'] = 5;
		}

		if (isset($this->request->post['image'])) {
			$data['image'] = $this->request->post['image'];
		} elseif (!empty($jade_testimonial_info)) {
			$data['image'] = $jade_testimonial_info['image'];
		} else {
			$data['image'] = '';
		}

		$this->load->model('tool/image');

		if (isset($this->request->post['image']) && is_file(DIR_IMAGE . $this->request->post['image'])) {
			$data['thumb'] = $this->model_tool_image->resize($this->request->post['image'], 100, 100);
		} elseif (!empty($jade_testimonial_info) && is_file(DIR_IMAGE . $jade_testimonial_info['image'])) {
			$data['thumb'] = $this->model_tool_image->resize($jade_testimonial_info['image'], 100, 100);
		} else {
			$data['thumb'] = $this->model_tool_image->resize('nouserpic.png', 100, 100);
		}

		$data['placeholder'] = $this->model_tool_image->resize('nouserpic.png', 100, 100);


		$data['user_token'] = $this->session->data['user_token'];

		$this->load->model('localisation/language');
		$data['languages'] = $this->model_localisation_language->getLanguages();

		$data['header'] = $this->load->controller('common/header');
		$data['column_left'] = $this->load->controller('common/column_left');
		$data['footer'] = $this->load->controller('common/footer');

		$this->config->set('template_engine', 'template');
		$this->response->setOutput($this->load->view('catalog/jade_testimonial_form', $data));
	}

	protected function validateForm() {
		if (!$this->user->hasPermission('modify', 'catalog/jade_testimonial')) {
			$this->error['warning'] = $this->language->get('error_permission');
		}

		foreach ($this->request->post['jade_testimonial_description'] as $language_id => $value) {
			if ((utf8_strlen($value['title']) < 3) || (utf8_strlen($value['title']) > 64)) {
				$this->error['title'][$language_id] = $this->language->get('error_title');
			}

			/*if ((utf8_strlen($value['destination']) < 2) || (utf8_strlen($value['destination']) > 128)) {
				$this->error['destination'][$language_id] = $this->language->get('error_destination');
			}*/
		}

		if ((utf8_strlen($this->request->post['author']) < 2) || (utf8_strlen($this->request->post['author']) > 64)) {
			$this->error['author'] = $this->language->get('error_author');
		}

		if ($this->error && !isset($this->error['warning'])) {
			$this->error['warning'] = $this->language->get('error_warning');
		}

		return !$this->error;
	}

	protected function validateDelete() {
		if (!$this->user->hasPermission('modify', 'catalog/jade_testimonial')) {
			$this->error['warning'] = $this->language->get('error_permission');
		}

		return !$this->error;
	}
}