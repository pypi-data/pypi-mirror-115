<?php
class ControllerExtensionModuleTopProducts extends Controller {
	private $error = array();

	public function index() {
		$this->load->language('extension/module/top_products');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->load->model('setting/module');

		if (($this->request->server['REQUEST_METHOD'] == 'POST') && $this->validate()) {
			if (!isset($this->request->get['module_id'])) {
				$this->model_setting_module->addModule('top_products', $this->request->post);
			} else {
				$this->model_setting_module->editModule($this->request->get['module_id'], $this->request->post);
			}

			$this->session->data['success'] = $this->language->get('text_success');

			$this->response->redirect($this->url->link('marketplace/extension', 'user_token=' . $this->session->data['user_token'] . '&type=module', true));
		}

		if (isset($this->error['warning'])) {
			$data['error_warning'] = $this->error['warning'];
		} else {
			$data['error_warning'] = '';
		}

		if (isset($this->error['name'])) {
			$data['error_name'] = $this->error['name'];
		} else {
			$data['error_name'] = '';
		}

		if (isset($this->error['product_image_size'])) {
			$data['error_product_image_size'] = $this->error['product_image_size'];
		} else {
			$data['error_product_image_size'] = '';
		}

		if (isset($this->error['testimonial_image_size'])) {
			$data['error_testimonial_image_size'] = $this->error['testimonial_image_size'];
		} else {
			$data['error_testimonial_image_size'] = '';
		}

		$data['breadcrumbs'] = array();

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('text_home'),
			'href' => $this->url->link('common/dashboard', 'user_token=' . $this->session->data['user_token'], true)
		);

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('text_extension'),
			'href' => $this->url->link('marketplace/extension', 'user_token=' . $this->session->data['user_token'] . '&type=module', true)
		);

		if (!isset($this->request->get['module_id'])) {
			$data['breadcrumbs'][] = array(
				'text' => $this->language->get('heading_title'),
				'href' => $this->url->link('extension/module/top_products', 'user_token=' . $this->session->data['user_token'], true)
			);
		} else {
			$data['breadcrumbs'][] = array(
				'text' => $this->language->get('heading_title'),
				'href' => $this->url->link('extension/module/top_products', 'user_token=' . $this->session->data['user_token'] . '&module_id=' . $this->request->get['module_id'], true)
			);
		}

		if (!isset($this->request->get['module_id'])) {
			$data['action'] = $this->url->link('extension/module/top_products', 'user_token=' . $this->session->data['user_token'], true);
		} else {
			$data['action'] = $this->url->link('extension/module/top_products', 'user_token=' . $this->session->data['user_token'] . '&module_id=' . $this->request->get['module_id'], true);
		}

		$data['cancel'] = $this->url->link('marketplace/extension', 'user_token=' . $this->session->data['user_token'] . '&type=module', true);

		if (isset($this->request->get['module_id']) && ($this->request->server['REQUEST_METHOD'] != 'POST')) {
			$module_info = $this->model_setting_module->getModule($this->request->get['module_id']);
		}

		$data['user_token'] = $this->session->data['user_token'];

		if (isset($this->request->post['name'])) {
			$data['name'] = $this->request->post['name'];
		} elseif (!empty($module_info)) {
			$data['name'] = $module_info['name'];
		} else {
			$data['name'] = '';
		}

		$this->load->model('catalog/product');

		$data['products'] = array();

		if (!empty($this->request->post['product'])) {
			$products = $this->request->post['product'];
		} elseif (!empty($module_info['product'])) {
			$products = $module_info['product'];
		} else {
			$products = array();
		}

		foreach ($products as $product_id) {
			$product_info = $this->model_catalog_product->getProduct($product_id);

			if ($product_info) {
				$data['products'][] = array(
					'product_id' => $product_info['product_id'],
					'name'       => $product_info['name']
				);
			}
		}

		if (isset($this->request->post['limit'])) {
			$data['limit'] = $this->request->post['limit'];
		} elseif (!empty($module_info)) {
			$data['limit'] = $module_info['limit'];
		} else {
			$data['limit'] = 5;
		}

		if (isset($this->request->post['width'])) {
			$data['width'] = $this->request->post['width'];
		} elseif (!empty($module_info)) {
			$data['width'] = $module_info['width'];
		} else {
			$data['width'] = 200;
		}

		if (isset($this->request->post['height'])) {
			$data['height'] = $this->request->post['height'];
		} elseif (!empty($module_info)) {
			$data['height'] = $module_info['height'];
		} else {
			$data['height'] = 200;
		}

		if (isset($this->request->post['product_status'])) {
			$data['product_status'] = $this->request->post['product_status'];
		} elseif (!empty($module_info)) {
			$data['product_status'] = $module_info['product_status'];
		} else {
			$data['product_status'] = 1;
		}

		if (isset($this->request->post['testimonial_width'])) {
			$data['testimonial_width'] = $this->request->post['testimonial_width'];
		} elseif (!empty($module_info['testimonial_width'])) {
			$data['testimonial_width'] = $module_info['testimonial_width'];
		} else {
			$data['testimonial_width'] = 140;
		}

		if (isset($this->request->post['testimonial_height'])) {
			$data['testimonial_height'] = $this->request->post['testimonial_height'];
		} elseif (!empty($module_info['testimonial_height'])) {
			$data['testimonial_height'] = $module_info['testimonial_height'];
		} else {
			$data['testimonial_height'] = 140;
		}

		if (isset($this->request->post['testimonial_status'])) {
			$data['testimonial_status'] = $this->request->post['testimonial_status'];
		} elseif (!empty($module_info)) {
			$data['testimonial_status'] = $module_info['testimonial_status'];
		} else {
			$data['testimonial_status'] = 1;
		}

		if (isset($this->request->post['testimonial_limit'])) {
			$data['testimonial_limit'] = $this->request->post['testimonial_limit'];
		} elseif (!empty($module_info)) {
			$data['testimonial_limit'] = $module_info['testimonial_limit'];
		} else {
			$data['testimonial_limit'] = 5;
		}

		if (isset($this->request->post['testimonial_desc_limit'])) {
			$data['testimonial_desc_limit'] = $this->request->post['testimonial_desc_limit'];
		} elseif (!empty($module_info)) {
			$data['testimonial_desc_limit'] = $module_info['testimonial_desc_limit'];
		} else {
			$data['testimonial_desc_limit'] = 5;
		}

		if (isset($this->request->post['status'])) {
			$data['status'] = $this->request->post['status'];
		} elseif (!empty($module_info)) {
			$data['status'] = $module_info['status'];
		} else {
			$data['status'] = '';
		}

		$data['header'] = $this->load->controller('common/header');
		$data['column_left'] = $this->load->controller('common/column_left');
		$data['footer'] = $this->load->controller('common/footer');

		$this->response->setOutput($this->load->view('extension/module/top_products', $data));
	}

	protected function validate() {
		if (!$this->user->hasPermission('modify', 'extension/module/top_products')) {
			$this->error['warning'] = $this->language->get('error_permission');
		}

		if ((utf8_strlen($this->request->post['name']) < 3) || (utf8_strlen($this->request->post['name']) > 64)) {
			$this->error['name'] = $this->language->get('error_name');
		}

		if (!$this->request->post['width']) {
			$this->error['product_image_size'] = $this->language->get('error_image_size');
		}

		if (!$this->request->post['height']) {
			$this->error['product_image_size'] = $this->language->get('error_image_size');
		}

		if (!$this->request->post['testimonial_width']) {
			$this->error['testimonial_image_size'] = $this->language->get('error_image_size');
		}

		if (!$this->request->post['testimonial_height']) {
			$this->error['testimonial_image_size'] = $this->language->get('error_image_size');
		}

		if ($this->error && !isset($this->error['warning'])) {
			$this->error['warning'] = $this->language->get('error_warning');
		}

		return !$this->error;
	}
}
