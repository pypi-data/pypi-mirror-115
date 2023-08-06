<?php
class ControllerextensionJadeFooterCopyright extends Controller {
	private $error = array();

	public function index() {
		$this->load->language('extension/jade_footer_copyright');

		$this->load->model('setting/setting');

		$this->document->setTitle($this->language->get('heading_title'));

		$this->document->addStyle('view/javascript/colorpicker/css/bootstrap-colorpicker.css');
		$this->document->addScript('view/javascript/colorpicker/js/bootstrap-colorpicker.js');

		if (($this->request->server['REQUEST_METHOD'] == 'POST') && $this->validate()) {
			$this->model_setting_setting->editSetting('jade_footer_copyright', $this->request->post);

			$this->session->data['success'] = $this->language->get('text_success');

			$this->response->redirect($this->url->link('extension/jade_footer_copyright', 'user_token=' . $this->session->data['user_token'], true));
		}

		$data['user_token'] = $this->session->data['user_token'];

		$data['heading_title'] = $this->language->get('heading_title');

		$data['text_edit'] = $this->language->get('text_edit');
		$data['text_enabled'] = $this->language->get('text_enabled');
		$data['text_disabled'] = $this->language->get('text_disabled');
		$data['text_control_panel'] = $this->language->get('text_control_panel');
		$data['text_left'] = $this->language->get('text_left');
		$data['text_center'] = $this->language->get('text_center');
		$data['text_right'] = $this->language->get('text_right');

		$data['entry_status'] = $this->language->get('entry_status');
		$data['entry_background_color'] = $this->language->get('entry_background_color');
		$data['entry_font_color'] = $this->language->get('entry_font_color');
		$data['entry_description'] = $this->language->get('entry_description');
		$data['entry_title'] = $this->language->get('entry_title');
		$data['entry_url'] = $this->language->get('entry_url');
		$data['entry_action'] = $this->language->get('entry_action');
		$data['entry_description_sizeclass'] = $this->language->get('entry_description_sizeclass');
		$data['entry_link_sizeclass'] = $this->language->get('entry_link_sizeclass');
		$data['entry_textalgin'] = $this->language->get('entry_textalgin');
		$data['entry_copyright_bg'] = $this->language->get('entry_copyright_bg');
		$data['entry_copyright_color'] = $this->language->get('entry_copyright_color');
		$data['entry_copyright_links_color'] = $this->language->get('entry_copyright_links_color');
		$data['entry_copyright_links_hover_color'] = $this->language->get('entry_copyright_links_hover_color');

		$data['text_yes'] = $this->language->get('text_yes');
		$data['text_no'] = $this->language->get('text_no');

		$data['tab_general'] = $this->language->get('tab_general');
		$data['tab_description'] = $this->language->get('tab_description');
		$data['tab_links'] = $this->language->get('tab_links');
		$data['tab_colors'] = $this->language->get('tab_colors');

		$data['button_save'] = $this->language->get('button_save');
		$data['button_cancel'] = $this->language->get('button_cancel');
		$data['button_remove'] = $this->language->get('button_remove');
		$data['button_informationlinks_add'] = $this->language->get('button_informationlinks_add');

		if (isset($this->error['warning'])) {
			$data['error_warning'] = $this->error['warning'];
		} else {
			$data['error_warning'] = '';
		}

		if (isset($this->error['informationlinks'])) {
			$data['error_informationlinks'] = $this->error['informationlinks'];
		} else {
			$data['error_informationlinks'] = '';
		}

		if (isset($this->session->data['success'])) {
			$data['success'] = $this->session->data['success'];

			unset($this->session->data['success']);
		} else {
			$data['success'] = '';
		}

		$data['breadcrumbs'] = array();

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('text_home'),
			'href' => $this->url->link('common/dashboard', 'user_token=' . $this->session->data['user_token'], true)
		);

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('heading_title'),
			'href' => $this->url->link('extension/jade_footer_copyright', 'user_token=' . $this->session->data['user_token'], true)
		);

		$data['action'] = $this->url->link('extension/jade_footer_copyright', 'user_token=' . $this->session->data['user_token'], true);

		$data['cancel'] = $this->url->link('common/dashboard', 'user_token=' . $this->session->data['user_token'], true);

		if (isset($this->request->post['jade_footer_copyright_status'])) {
			$data['jade_footer_copyright_status'] = $this->request->post['jade_footer_copyright_status'];
		} else {
			$data['jade_footer_copyright_status'] = $this->config->get('jade_footer_copyright_status');
		}

		if (isset($this->request->post['jade_footer_copyright_background_color'])) {
			$data['jade_footer_copyright_background_color'] = $this->request->post['jade_footer_copyright_background_color'];
		} else {
			$data['jade_footer_copyright_background_color'] = $this->config->get('jade_footer_copyright_background_color');
		}

		if (isset($this->request->post['jade_footer_copyright_font_color'])) {
			$data['jade_footer_copyright_font_color'] = $this->request->post['jade_footer_copyright_font_color'];
		} else {
			$data['jade_footer_copyright_font_color'] = $this->config->get('jade_footer_copyright_font_color');
		}

		if (isset($this->request->post['jade_footer_copyright_description'])) {
			$data['jade_footer_copyright_description'] = $this->request->post['jade_footer_copyright_description'];
		} else {
			$data['jade_footer_copyright_description'] = (array)$this->config->get('jade_footer_copyright_description');
		}

		if (isset($this->request->post['jade_footer_copyright_informationlinks'])) {
			$data['informationlinks'] = $this->request->post['jade_footer_copyright_informationlinks'];
		} else {
			$data['informationlinks'] = (array)$this->config->get('jade_footer_copyright_informationlinks');
		}

		if (isset($this->request->post['jade_footer_copyright_description_sizeclass'])) {
			$data['jade_footer_copyright_description_sizeclass'] = $this->request->post['jade_footer_copyright_description_sizeclass'];
		} else {
			$data['jade_footer_copyright_description_sizeclass'] = $this->config->get('jade_footer_copyright_description_sizeclass');
		}

		if (isset($this->request->post['jade_footer_copyright_link_sizeclass'])) {
			$data['jade_footer_copyright_link_sizeclass'] = $this->request->post['jade_footer_copyright_link_sizeclass'];
		} else {
			$data['jade_footer_copyright_link_sizeclass'] = $this->config->get('jade_footer_copyright_link_sizeclass');
		}

		if (isset($this->request->post['jade_footer_copyright_textalgin'])) {
			$data['jade_footer_copyright_textalgin'] = $this->request->post['jade_footer_copyright_textalgin'];
		} else if ($this->config->get('jade_footer_copyright_textalgin')) {
			$data['jade_footer_copyright_textalgin'] = $this->config->get('jade_footer_copyright_textalgin');
		} else {
			$data['jade_footer_copyright_textalgin'] = 'left';
		}


		if (isset($this->request->post['jade_footer_copyright_bg'])) {
			$data['jade_footer_copyright_bg'] = $this->request->post['jade_footer_copyright_bg'];
		} else {
			$data['jade_footer_copyright_bg'] = $this->config->get('jade_footer_copyright_bg');
		}

		if (isset($this->request->post['jade_footer_copyright_color'])) {
			$data['jade_footer_copyright_color'] = $this->request->post['jade_footer_copyright_color'];
		} else {
			$data['jade_footer_copyright_color'] = $this->config->get('jade_footer_copyright_color');
		}

		if (isset($this->request->post['jade_footer_copyright_links_color'])) {
			$data['jade_footer_copyright_links_color'] = $this->request->post['jade_footer_copyright_links_color'];
		} else {
			$data['jade_footer_copyright_links_color'] = $this->config->get('jade_footer_copyright_links_color');
		}

		if (isset($this->request->post['jade_footer_copyright_links_hover_color'])) {
			$data['jade_footer_copyright_links_hover_color'] = $this->request->post['jade_footer_copyright_links_hover_color'];
		} else {
			$data['jade_footer_copyright_links_hover_color'] = $this->config->get('jade_footer_copyright_links_hover_color');
		}

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

		$this->load->model('localisation/language');
		$data['languages'] = $this->model_localisation_language->getLanguages();

		$data['header'] = $this->load->controller('common/header');
		$data['column_left'] = $this->load->controller('common/column_left');
		$data['footer'] = $this->load->controller('common/footer');

		$this->config->set('template_engine', 'template');
		$this->response->setOutput($this->load->view('extension/jade_footer_copyright', $data));
	}

	protected function validate() {
		if (!$this->user->hasPermission('modify', 'extension/jade_footer_copyright')) {
			$this->error['warning'] = $this->language->get('error_permission');
		}

		if (isset($this->request->post['jade_footer_copyright_informationlinks'])) {
			foreach ($this->request->post['jade_footer_copyright_informationlinks'] as $informationlinks_row => $informationlinks) {
				foreach ($informationlinks['informationlinks_description'] as $language_id => $informationlinks_description) {
					if ((utf8_strlen($informationlinks_description['title']) < 1) || (utf8_strlen($informationlinks_description['title']) > 255)) {
						$this->error['informationlinks'][$informationlinks_row][$language_id] = $this->language->get('error_informationlinks_title');
					}
				}
			}
		}

		if ($this->error && !isset($this->error['warning'])) {
			$this->error['warning'] = $this->language->get('error_warning');
		}

		return !$this->error;
	}
}