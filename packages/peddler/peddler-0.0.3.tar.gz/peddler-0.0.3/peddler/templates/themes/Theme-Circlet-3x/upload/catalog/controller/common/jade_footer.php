<?php
class ControllerCommonJadeFooter extends Controller {
	public function index() {
		$this->load->language('common/jade_footer');

		$this->load->model('extension/jade_footer');

		$this->load->model('tool/image');

		$data['scripts'] = $this->document->getScripts('footer');

		$this->document->addStyle('catalog/view/theme/circlet/stylesheet/jadefooter/jadefooter.css');

		// Whos Online
		if ($this->config->get('config_customer_online')) {
			$this->load->model('tool/online');

			if (isset($this->request->server['REMOTE_ADDR'])) {
				$ip = $this->request->server['REMOTE_ADDR'];
			} else {
				$ip = '';
			}

			if (isset($this->request->server['HTTP_HOST']) && isset($this->request->server['REQUEST_URI'])) {
				$url = 'http://' . $this->request->server['HTTP_HOST'] . $this->request->server['REQUEST_URI'];
			} else {
				$url = '';
			}

			if (isset($this->request->server['HTTP_REFERER'])) {
				$referer = $this->request->server['HTTP_REFERER'];
			} else {
				$referer = '';
			}

			$this->model_tool_online->addOnline($ip, $this->customer->getId(), $url, $referer);
		}



		/* Main Footer Starts */

		if ($this->request->server['HTTPS']) {
			$server = $this->config->get('config_ssl');
		} else {
			$server = $this->config->get('config_url');
		}

		if (is_file(DIR_IMAGE . $this->config->get('jade_footer_logo'))) {
			$data['footer_logo'] = $server . 'image/' . $this->config->get('jade_footer_logo');
		} else {
			$data['footer_logo'] = '';
		}

		$data['language_id'] = $this->config->get('config_language_id');


		$data['home_link'] = $this->url->link('common/home', '', true);

		$jade_customfooters = $this->model_extension_jade_footer->getJadeCustomfooters();

		$data['jade_customfooters'] = array();
		foreach($jade_customfooters as $jade_customfooter) {

			$payments_table_data = array();
			if($jade_customfooter['type_code'] == 'payments_icons' && !empty($jade_customfooter['payments_table'])) {
				$payments_tables = json_decode($jade_customfooter['payments_table'], 1);

				foreach($payments_tables as $payments_table) {
					$payment_image = $this->model_tool_image->resize($payments_table['image'], 46, 46);

					$payments_table_data[] = array(
						'payments_description'			=> isset($payments_table['payments_description']) ? $payments_table['payments_description'] : array(),
						'image'							=> $payment_image,
					);
				}
			}

			$appicons_table_data = array();
			if($jade_customfooter['type_code'] == 'app_icons' && !empty($jade_customfooter['appicons_table'])) {
				$appicons_tables = json_decode($jade_customfooter['appicons_table'], 1);

				foreach($appicons_tables as $appicons_table) {
					$appicons_image = $this->model_tool_image->resize($appicons_table['image'], 130, 43);

					$appicons_table_data[] = array(
						'appicons_description'			=> isset($appicons_table['appicons_description']) ? $appicons_table['appicons_description'] : array(),
						'image'							=> $appicons_image,
					);
				}
			}


			$editor_description_data = '';
			if($jade_customfooter['type_code'] == 'editor' && !empty($jade_customfooter['editor_description'])) {
				$editor_description = json_decode($jade_customfooter['editor_description'], 1);

				$editor_description_data = isset($editor_description[$this->config->get('config_language_id')]['description']) ? html_entity_decode($editor_description[$this->config->get('config_language_id')]['description'], ENT_QUOTES, 'UTF-8') : '';
			}

			$newsletter_table_data = array();
			if($jade_customfooter['type_code'] == 'newsletter'  && !empty($jade_customfooter['editor_description'])) {
				$newsletter_table = json_decode($jade_customfooter['newsletter_table'], 1);
				$newsletter_table_data['placeholder'] = isset($newsletter_table[$this->config->get('config_language_id')]['placeholder']) ? $newsletter_table[$this->config->get('config_language_id')]['placeholder'] : '';

				$newsletter_table_data['button_text'] = isset($newsletter_table[$this->config->get('config_language_id')]['button_text']) ? $newsletter_table[$this->config->get('config_language_id')]['button_text'] : '';

				$newsletter_table_data['hotline_title'] = isset($newsletter_table[$this->config->get('config_language_id')]['hotline_title']) ? $newsletter_table[$this->config->get('config_language_id')]['hotline_title'] : '';

				$newsletter_table_data['hotline_description'] = isset($newsletter_table[$this->config->get('config_language_id')]['hotline_description']) ? html_entity_decode($newsletter_table[$this->config->get('config_language_id')]['hotline_description'], ENT_QUOTES, 'UTF-8') : '';
			}

			$data['jade_customfooters'][] = array(
				'type_code'					=> $jade_customfooter['type_code'],
				'title'						=> $jade_customfooter['title'],
				'size_class'				=> $jade_customfooter['size_class'],
				'contactdetail_table'		=> !empty($jade_customfooter['contactdetail_table']) ? json_decode($jade_customfooter['contactdetail_table'], 1) : array(),
				'accountlinks_table'		=> !empty($jade_customfooter['accountlinks_table']) ? json_decode($jade_customfooter['accountlinks_table'], 1) : array(),
				'informationlinks_table'	=> !empty($jade_customfooter['informationlinks_table']) ? json_decode($jade_customfooter['informationlinks_table'], 1) : array(),
				'sociallinks_table'			=> !empty($jade_customfooter['sociallinks_table']) ? json_decode($jade_customfooter['sociallinks_table'], 1) : array(),
				'newsletter_table' 			=> $newsletter_table_data,
				'payments_table'			=> $payments_table_data,
				'appicons_table'			=> $appicons_table_data,
				'editor_description'		=> $editor_description_data,
			);
		}

		$data['footer_bgcolor'] = $this->config->get('jade_footer_bgcolor');
		$data['footer_heading_color'] = $this->config->get('jade_footer_heading_color');
		$data['footer_icon_color'] = $this->config->get('jade_footer_icon_color');
		$data['footer_text_color'] = $this->config->get('jade_footer_text_color');
		$data['footer_link_hover_color'] = $this->config->get('jade_footer_link_hover_color');
		$data['footer_social_media_bgcolor'] = $this->config->get('jade_footer_social_media_bgcolor');
		$data['footer_social_media_color'] = $this->config->get('jade_footer_social_media_color');
		$data['footer_social_media_hover_bgcolor'] = $this->config->get('jade_footer_social_media_hover_bgcolor');
		$data['footer_social_media_hover_color'] = $this->config->get('jade_footer_social_media_hover_color');
		$data['footer_newsletter_btn_bg'] = $this->config->get('jade_footer_newsletter_btn_bg');
		$data['footer_newsletter_btn_color'] = $this->config->get('jade_footer_newsletter_btn_color');
		$data['footer_newsletter_input_border_color'] = $this->config->get('jade_footer_newsletter_input_border_color');
		$data['footer_hot_line_color'] = $this->config->get('jade_footer_hot_line_color');
		/* Main Footer Ends */

		/* Copyright Footer Starts */
		$data['copyright_status'] = $this->config->get('jade_footer_copyright_status');
		$copyright_description = $this->config->get('jade_footer_copyright_description');

		$data['copyright_description'] = isset($copyright_description[$this->config->get('config_language_id')]['description']) ? html_entity_decode($copyright_description[$this->config->get('config_language_id')]['description'], ENT_QUOTES, 'UTF-8') : '';

		$data['copyright_description_strip_tags'] = trim(strip_tags($data['copyright_description']));

		$informationlinks = (array)$this->config->get('jade_footer_copyright_informationlinks');

		$data['informationlinks'] = array();
		foreach ($informationlinks as $informationlink) {
			$data['informationlinks'][] = array(
				'title'		=> isset($informationlink['informationlinks_description'][$this->config->get('config_language_id')]['title']) ? $informationlink['informationlinks_description'][$this->config->get('config_language_id')]['title'] : '',
				'url'		=> $informationlink['url'],
			);
		}

		$data['description_sizeclass'] = $this->config->get('jade_footer_copyright_description_sizeclass');
		$data['link_sizeclass'] = $this->config->get('jade_footer_copyright_link_sizeclass');
		$data['custom_links_textalgin'] = $this->config->get('jade_footer_copyright_textalgin');

		$data['footer_copyright_bg'] = $this->config->get('jade_footer_copyright_bg');
		$data['footer_copyright_color'] = $this->config->get('jade_footer_copyright_color');
		$data['footer_copyright_links_color'] = $this->config->get('jade_footer_copyright_links_color');
		$data['footer_copyright_links_hover_color'] = $this->config->get('jade_footer_copyright_links_hover_color');
		/* Copyright Footer Ends */

		if(VERSION < '2.2.0.0') {
			if (file_exists(DIR_TEMPLATE . $this->config->get('config_template') . '/template/common/jade_footer.tpl')) {
				return $this->load->view($this->config->get('config_template') . '/template/common/jade_footer.tpl', $data);
			} else {
				return $this->load->view('default/template/common/jade_footer.tpl', $data);
			}
		} else {
			return $this->load->view('common/jade_footer', $data);
		}
	}

	public function submitnewsletter() {
		$json = array();

		$this->load->language('common/jade_footer');

		$this->load->model('extension/jade_footer');

		if ((utf8_strlen($this->request->post['newsletter_email']) > 96) || !filter_var($this->request->post['newsletter_email'], FILTER_VALIDATE_EMAIL)) {
			$json['warning'] = $this->language->get('error_newsletter_email');
		}

		if ($this->model_extension_jade_footer->getTotalSubscribersByEmail($this->request->post['newsletter_email'])) {
			$json['warning'] = $this->language->get('error_email_exists');
		}

		if(!$json) {
			$this->model_extension_jade_footer->addNewsletterEmail($this->request->post['newsletter_email']);

			$json['success'] = $this->language->get('text_email_success');
		}


		$this->response->addHeader('Content-Type: application/json');
		$this->response->setOutput(json_encode($json));
	}
}
