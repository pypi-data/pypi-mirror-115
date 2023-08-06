<?php
class ControllerExtensionModuleMultiBanner extends Controller {
	public function index($setting) {
		if ($this->config->get('config_theme') == 'default') {
			$theme = $this->config->get('theme_default_directory');
		} else {
			$theme = $this->config->get('config_theme');
		}
		if ('circlet' != $theme) {
			return;
		}

		static $module = 0;

		if ($this->request->server['HTTPS']) {
			$server = $this->config->get('config_ssl');
		} else {
			$server = $this->config->get('config_url');
		}


		$this->load->model('tool/image');

		$data['columns'] = array();

		if(isset($setting['columns'])) {
			foreach ($setting['columns'] as $column) {
				$column_value_data = array();

				foreach($column['column_value'] as $value) {
					if (is_file(DIR_IMAGE . $value['image'])) {
						if(empty($value['width']) || empty($value['height'])) {
							$image = $server . 'image/'. $value['image'];
						} else {
							$image = $this->model_tool_image->resize($value['image'], $value['width'], $value['height']);
						}
					} else {
						$image = '';
					}

					if($image && $value['status']) {
						$column_value_data[] = array(
							'link'				=> $value['link'],
							'image'				=> $image,
							'title'				=> isset($value['description'][$this->config->get('config_language_id')]['title']) ? $value['description'][$this->config->get('config_language_id')]['title'] : '',
						);
					}
				}

				$data['columns'][] = array(
					'size' 			=> $column['size'],
					'column_value' 	=> $column_value_data,
				);
			}
		}

		$data['module'] = $module++;

		return $this->load->view('extension/module/multi_banner', $data);
	}
}