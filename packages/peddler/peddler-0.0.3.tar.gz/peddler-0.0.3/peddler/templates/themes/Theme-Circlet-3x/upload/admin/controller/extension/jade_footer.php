<?php
class ControllerextensionJadeFooter extends Controller {
	private $error = array();

	public function index() {
		$this->load->language('extension/jade_footer');

		$this->load->model('setting/setting');

		$this->load->model('tool/image');

		$this->load->model('extension/jade_customfooter');

		$this->model_extension_jade_customfooter->CreateJadeFooterTable();

		$this->document->setTitle($this->language->get('heading_title'));

		$this->document->addStyle('view/javascript/colorpicker/css/bootstrap-colorpicker.css');
		$this->document->addScript('view/javascript/colorpicker/js/bootstrap-colorpicker.js');

		if (($this->request->server['REQUEST_METHOD'] == 'POST') && $this->validate()) {
			$this->model_setting_setting->editSetting('jade_footer', $this->request->post);

			$this->session->data['success'] = $this->language->get('text_success');

			$this->response->redirect($this->url->link('extension/jade_footer', 'user_token=' . $this->session->data['user_token'], true));
		}

		$data['user_token'] = $this->session->data['user_token'];

		$data['heading_title'] = $this->language->get('heading_title');

		$data['text_edit'] = $this->language->get('text_edit');
		$data['text_enabled'] = $this->language->get('text_enabled');
		$data['text_disabled'] = $this->language->get('text_disabled');
		$data['text_control_panel'] = $this->language->get('text_control_panel');

		$data['entry_status'] = $this->language->get('entry_status');
		$data['entry_logo'] = $this->language->get('entry_logo');
		$data['entry_bgcolor'] = $this->language->get('entry_bgcolor');
		$data['entry_heading_color'] = $this->language->get('entry_heading_color');
		$data['entry_icon_color'] = $this->language->get('entry_icon_color');
		$data['entry_text_color'] = $this->language->get('entry_text_color');
		$data['entry_link_hover_color'] = $this->language->get('entry_link_hover_color');
		$data['entry_social_media_bgcolor'] = $this->language->get('entry_social_media_bgcolor');
		$data['entry_social_media_color'] = $this->language->get('entry_social_media_color');
		$data['entry_social_media_hover_bgcolor'] = $this->language->get('entry_social_media_hover_bgcolor');
		$data['entry_social_media_hover_color'] = $this->language->get('entry_social_media_hover_color');
		$data['entry_newsletter_btn_bg'] = $this->language->get('entry_newsletter_btn_bg');
		$data['entry_newsletter_btn_color'] = $this->language->get('entry_newsletter_btn_color');
		$data['entry_newsletter_input_border_color'] = $this->language->get('entry_newsletter_input_border_color');
		$data['entry_hot_line_color'] = $this->language->get('entry_hot_line_color');

		$data['text_yes'] = $this->language->get('text_yes');
		$data['text_no'] = $this->language->get('text_no');

		$data['tab_general'] = $this->language->get('tab_general');
		$data['tab_colors'] = $this->language->get('tab_colors');
		$data['tab_support'] = $this->language->get('tab_support');

		$data['button_save'] = $this->language->get('button_save');
		$data['button_cancel'] = $this->language->get('button_cancel');

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

		$data['breadcrumbs'] = array();

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('text_home'),
			'href' => $this->url->link('common/dashboard', 'user_token=' . $this->session->data['user_token'], true)
		);

		$data['breadcrumbs'][] = array(
			'text' => $this->language->get('heading_title'),
			'href' => $this->url->link('extension/jade_footer', 'user_token=' . $this->session->data['user_token'], true)
		);

		$data['action'] = $this->url->link('extension/jade_footer', 'user_token=' . $this->session->data['user_token'], true);

		$data['cancel'] = $this->url->link('common/dashboard', 'user_token=' . $this->session->data['user_token'], true);

		if (isset($this->request->post['jade_footer_status'])) {
			$data['jade_footer_status'] = $this->request->post['jade_footer_status'];
		} else {
			$data['jade_footer_status'] = $this->config->get('jade_footer_status');
		}

		if (isset($this->request->post['jade_footer_logo'])) {
			$data['jade_footer_logo'] = $this->request->post['jade_footer_logo'];
		} else {
			$data['jade_footer_logo'] = $this->config->get('jade_footer_logo');
		}

		if (isset($this->request->post['jade_footer_logo']) && is_file(DIR_IMAGE . $this->request->post['jade_footer_logo'])) {
			$data['logo'] = $this->model_tool_image->resize($this->request->post['jade_footer_logo'], 100, 100);
		} elseif ($this->config->get('jade_footer_logo') && is_file(DIR_IMAGE . $this->config->get('jade_footer_logo'))) {
			$data['logo'] = $this->model_tool_image->resize($this->config->get('jade_footer_logo'), 100, 100);
		} else {
			$data['logo'] = $this->model_tool_image->resize('no_image.png', 100, 100);
		}

		if (isset($this->request->post['jade_footer_bgcolor'])) {
			$data['jade_footer_bgcolor'] = $this->request->post['jade_footer_bgcolor'];
		} else {
			$data['jade_footer_bgcolor'] = $this->config->get('jade_footer_bgcolor');
		}

		if (isset($this->request->post['jade_footer_heading_color'])) {
			$data['jade_footer_heading_color'] = $this->request->post['jade_footer_heading_color'];
		} else {
			$data['jade_footer_heading_color'] = $this->config->get('jade_footer_heading_color');
		}

		if (isset($this->request->post['jade_footer_icon_color'])) {
			$data['jade_footer_icon_color'] = $this->request->post['jade_footer_icon_color'];
		} else {
			$data['jade_footer_icon_color'] = $this->config->get('jade_footer_icon_color');
		}

		if (isset($this->request->post['jade_footer_text_color'])) {
			$data['jade_footer_text_color'] = $this->request->post['jade_footer_text_color'];
		} else {
			$data['jade_footer_text_color'] = $this->config->get('jade_footer_text_color');
		}

		if (isset($this->request->post['jade_footer_link_hover_color'])) {
			$data['jade_footer_link_hover_color'] = $this->request->post['jade_footer_link_hover_color'];
		} else {
			$data['jade_footer_link_hover_color'] = $this->config->get('jade_footer_link_hover_color');
		}

		if (isset($this->request->post['jade_footer_social_media_bgcolor'])) {
			$data['jade_footer_social_media_bgcolor'] = $this->request->post['jade_footer_social_media_bgcolor'];
		} else {
			$data['jade_footer_social_media_bgcolor'] = $this->config->get('jade_footer_social_media_bgcolor');
		}

		if (isset($this->request->post['jade_footer_social_media_color'])) {
			$data['jade_footer_social_media_color'] = $this->request->post['jade_footer_social_media_color'];
		} else {
			$data['jade_footer_social_media_color'] = $this->config->get('jade_footer_social_media_color');
		}

		if (isset($this->request->post['jade_footer_social_media_hover_bgcolor'])) {
			$data['jade_footer_social_media_hover_bgcolor'] = $this->request->post['jade_footer_social_media_hover_bgcolor'];
		} else {
			$data['jade_footer_social_media_hover_bgcolor'] = $this->config->get('jade_footer_social_media_hover_bgcolor');
		}

		if (isset($this->request->post['jade_footer_social_media_hover_color'])) {
			$data['jade_footer_social_media_hover_color'] = $this->request->post['jade_footer_social_media_hover_color'];
		} else {
			$data['jade_footer_social_media_hover_color'] = $this->config->get('jade_footer_social_media_hover_color');
		}

		if (isset($this->request->post['jade_footer_newsletter_btn_bg'])) {
			$data['jade_footer_newsletter_btn_bg'] = $this->request->post['jade_footer_newsletter_btn_bg'];
		} else {
			$data['jade_footer_newsletter_btn_bg'] = $this->config->get('jade_footer_newsletter_btn_bg');
		}

		if (isset($this->request->post['jade_footer_newsletter_btn_color'])) {
			$data['jade_footer_newsletter_btn_color'] = $this->request->post['jade_footer_newsletter_btn_color'];
		} else {
			$data['jade_footer_newsletter_btn_color'] = $this->config->get('jade_footer_newsletter_btn_color');
		}

		if (isset($this->request->post['jade_footer_newsletter_input_border_color'])) {
			$data['jade_footer_newsletter_input_border_color'] = $this->request->post['jade_footer_newsletter_input_border_color'];
		} else {
			$data['jade_footer_newsletter_input_border_color'] = $this->config->get('jade_footer_newsletter_input_border_color');
		}

		if (isset($this->request->post['jade_footer_hot_line_color'])) {
			$data['jade_footer_hot_line_color'] = $this->request->post['jade_footer_hot_line_color'];
		} else {
			$data['jade_footer_hot_line_color'] = $this->config->get('jade_footer_hot_line_color');
		}


		$data['placeholder'] = $this->model_tool_image->resize('no_image.png', 100, 100);

		$data['header'] = $this->load->controller('common/header');
		$data['column_left'] = $this->load->controller('common/column_left');
		$data['footer'] = $this->load->controller('common/footer');

		$this->config->set('template_engine', 'template');
		$this->response->setOutput($this->load->view('extension/jade_footer', $data));
	}

	protected function validate() {
		if (!$this->user->hasPermission('modify', 'extension/jade_footer')) {
			$this->error['warning'] = $this->language->get('error_permission');
		}

		return !$this->error;
	}
}