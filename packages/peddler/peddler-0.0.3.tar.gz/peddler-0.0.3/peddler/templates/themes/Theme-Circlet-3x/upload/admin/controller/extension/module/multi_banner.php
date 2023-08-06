<?php
class ControllerExtensionModuleMultiBanner extends Controller {
	private $error = array();

	public function index() {
		$this->load->language('extension/module/multi_banner');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->load->model('setting/module');

		$this->load->model('tool/image');

		if (($this->request->server['REQUEST_METHOD'] == 'POST') && $this->validate()) {
			if (!isset($this->request->get['module_id'])) {
				$this->model_setting_module->addModule('multi_banner', $this->request->post);
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

		if (isset($this->error['width'])) {
			$data['error_width'] = $this->error['width'];
		} else {
			$data['error_width'] = '';
		}

		if (isset($this->error['height'])) {
			$data['error_height'] = $this->error['height'];
		} else {
			$data['error_height'] = '';
		}

		if (isset($this->error['column_value'])) {
			$data['error_column_value'] = $this->error['column_value'];
		} else {
			$data['error_column_value'] = array();
		}

		if (isset($this->error['column_value_image'])) {
			$data['error_column_value_image'] = $this->error['column_value_image'];
		} else {
			$data['error_column_value_image'] = array();
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
				'href' => $this->url->link('extension/module/multi_banner', 'user_token=' . $this->session->data['user_token'], true)
			);
		} else {
			$data['breadcrumbs'][] = array(
				'text' => $this->language->get('heading_title'),
				'href' => $this->url->link('extension/module/multi_banner', 'user_token=' . $this->session->data['user_token'] . '&module_id=' . $this->request->get['module_id'], true)
			);
		}

		if (!isset($this->request->get['module_id'])) {
			$data['action'] = $this->url->link('extension/module/multi_banner', 'user_token=' . $this->session->data['user_token'], true);
		} else {
			$data['action'] = $this->url->link('extension/module/multi_banner', 'user_token=' . $this->session->data['user_token'] . '&module_id=' . $this->request->get['module_id'], true);
		}

		$data['cancel'] = $this->url->link('marketplace/extension', 'user_token=' . $this->session->data['user_token'] . '&type=module', true);

		if (isset($this->request->get['module_id']) && ($this->request->server['REQUEST_METHOD'] != 'POST')) {
			$module_info = $this->model_setting_module->getModule($this->request->get['module_id']);
		}

		if (isset($this->request->post['name'])) {
			$data['name'] = $this->request->post['name'];
		} elseif (!empty($module_info)) {
			$data['name'] = $module_info['name'];
		} else {
			$data['name'] = '';
		}

		if (isset($this->request->post['status'])) {
			$data['status'] = $this->request->post['status'];
		} elseif (!empty($module_info)) {
			$data['status'] = $module_info['status'];
		} else {
			$data['status'] = '';
		}

		if (isset($this->request->post['columns'])) {
			$columns = $this->request->post['columns'];
		} elseif (!empty($module_info['columns'])) {
			$columns = (array)$module_info['columns'];
		} else {
			$columns = array();
		}

		$data['columns'] = array();
		foreach($columns as $column) {

			$column_value_data =array();
			if(!empty($column['column_value'])) {
				foreach($column['column_value'] as $column_value) {
					if (is_file(DIR_IMAGE . $column_value['image'])) {
						$image = $column_value['image'];
						$thumb = $this->model_tool_image->resize($column_value['image'], 100, 100);
					} else {
						$image = '';
						$thumb = $this->model_tool_image->resize('no_image.png', 100, 100);
					}

					$column_value_data[] = array(
						'thumb'				=> $thumb,
						'image'				=> $image,
						'link'				=> $column_value['link'],
						'width'				=> $column_value['width'],
						'height'			=> $column_value['height'],
						'status'			=> isset($column_value['status']) ? $column_value['status'] : '',
						'description'		=> isset($column_value['description']) ? $column_value['description'] : array(),
					);
				}
			}

			$data['columns'][] = array(
				'size'					=> $column['size'],
				'column_value'			=> $column_value_data,
			);
		}

		$data['column_sizes'] = array();

		for($i=1; $i <= 12; $i++) {
			$data['column_sizes'][] = array(
				'size'			=> 'col-sm-'. $i,
			);
		}

		$data['placeholder'] = $this->model_tool_image->resize('no_image.png', 100, 100);

		$this->load->model('localisation/language');
		$data['languages'] = $this->model_localisation_language->getLanguages();

		$data['header'] = $this->load->controller('common/header');
		$data['column_left'] = $this->load->controller('common/column_left');
		$data['footer'] = $this->load->controller('common/footer');

		$this->response->setOutput($this->load->view('extension/module/multi_banner', $data));
	}

	protected function validate() {
		if (!$this->user->hasPermission('modify', 'extension/module/multi_banner')) {
			$this->error['warning'] = $this->language->get('error_permission');
		}

		if ((utf8_strlen($this->request->post['name']) < 3) || (utf8_strlen($this->request->post['name']) > 64)) {
			$this->error['name'] = $this->language->get('error_name');
		}

		if(!isset($this->request->post['columns'])) {
			$this->error['warning'] = $this->language->get('error_columns');
		} else {
			foreach ($this->request->post['columns'] as $key => $column_value) {
				if(isset($column_value['column_value'])) {
					foreach ($column_value['column_value'] as $value_key => $value) {
						if(empty($value['image'])) {
							$this->error['column_value_image'][$key][$value_key] = $this->language->get('error_image');
						}
					}
				} else {
					$this->error['column_value'][$key] = $this->language->get('error_column_value');
				}
			}
		}

		if ($this->error && !isset($this->error['warning'])) {
			$this->error['warning'] = $this->language->get('error_warning');
		}

		return !$this->error;
	}
}