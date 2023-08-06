<?php
class ControllerExtensionJcirclet extends Controller {
	private $error = array();

	public function index() {
		$this->load->language('extension/jcirclet');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->load->model('setting/setting');

		$this->load->model('tool/image');

		if (($this->request->server['REQUEST_METHOD'] == 'POST') && $this->validate()) {
			$this->model_setting_setting->editSetting('jcirclet', $this->request->post);

			$this->session->data['success'] = $this->language->get('text_success');

			$this->response->redirect($this->url->link('extension/jcirclet', 'user_token=' . $this->session->data['user_token'], true));
		}

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

		if (isset($this->error['url_title'])) {
			$data['error_url_title'] = $this->error['url_title'];
		} else {
			$data['error_url_title'] = array();
		}

		$data['breadcrumbs'] = array();

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('text_home'),
			'href' => $this->url->link('common/dashboard', 'user_token=' . $this->session->data['user_token'], true)
		);

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('heading_title'),
			'href' => $this->url->link('extension/jcirclet', 'user_token=' . $this->session->data['user_token'], true)
		);

		$data['action'] = $this->url->link('extension/jcirclet', 'user_token=' . $this->session->data['user_token'], true);

		$data['cancel'] = $this->url->link('common/dashboard', 'user_token=' . $this->session->data['user_token'] . '&type=module', true);



		if (isset($this->request->post['jcirclet_banner'])) {
			$data['jcirclet_banner'] = $this->request->post['jcirclet_banner'];
		} else {
			$data['jcirclet_banner'] = $this->config->get('jcirclet_banner');
		}

		if (isset($this->request->post['jcirclet_banner']) && is_file(DIR_IMAGE . $this->request->post['jcirclet_banner'])) {
			$data['banner'] = $this->model_tool_image->resize($this->request->post['jcirclet_banner'], 100, 100);
		} elseif ($this->config->get('jcirclet_banner') && is_file(DIR_IMAGE . $this->config->get('jcirclet_banner'))) {
			$data['banner'] = $this->model_tool_image->resize($this->config->get('jcirclet_banner'), 100, 100);
		} else {
			$data['banner'] = $this->model_tool_image->resize('no_image.png', 100, 100);
		}

		$data['placeholder'] = $this->model_tool_image->resize('no_image.png', 100, 100);


		$this->load->model('localisation/language');
		$data['languages'] = $this->model_localisation_language->getLanguages();
		$data['languageid'] = $this->config->get('config_language_id');

		$data['header'] = $this->load->controller('common/header');
		$data['column_left'] = $this->load->controller('common/column_left');
		$data['footer'] = $this->load->controller('common/footer');

		$this->response->setOutput($this->load->view('extension/jcirclet', $data));
	}

	protected function validate() {
		if (!$this->user->hasPermission('modify', 'extension/jcirclet')) {
			$this->error['warning'] = $this->language->get('error_permission');
		}


		if ($this->error && !isset($this->error['warning'])) {
			$this->error['warning'] = $this->language->get('error_warning');
		}

		return !$this->error;
	}
}