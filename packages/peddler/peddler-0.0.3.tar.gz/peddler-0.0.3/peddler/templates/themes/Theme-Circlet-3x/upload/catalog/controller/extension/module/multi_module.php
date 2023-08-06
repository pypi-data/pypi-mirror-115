<?php
class ControllerExtensionModuleMultiModule extends Controller {
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

		$this->load->model('catalog/product');

		$this->load->model('catalog/jade_circlet');

		$this->load->model('tool/image');

		if (!$setting['limit']) {
			$setting['limit'] = 4;
		}

		$data['columns'] = array();



		if(!empty($setting['columns'])) {
			$count = 1;
			foreach ($setting['columns'] as $column) {
				$products = array();

				switch ($column['module_type']) {
					case 'latest_products':
						$lastest_filter_data = array(
							'sort'  => 'p.date_added',
							'order' => 'DESC',
							'start' => 0,
							'limit' => $setting['limit']
						);

						$results = $this->model_catalog_product->getProducts($lastest_filter_data);

						foreach ($results as $result) {
							if ($result['image']) {
								$image = $this->model_tool_image->resize($result['image'], $setting['width'], $setting['height']);
							} else {
								$image = $this->model_tool_image->resize('placeholder.png', $setting['width'], $setting['height']);
							}

							$additional_image_row = $this->model_catalog_jade_circlet->getProductAdditionalFirstImage($result['product_id']);

							if (!empty($additional_image_row['image'])) {
								$additional_image = $this->model_tool_image->resize($additional_image_row['image'], $setting['width'], $setting['height']);
							} else {
								$additional_image = '';
							}

							if ($this->customer->isLogged() || !$this->config->get('config_customer_price')) {
								$price = $this->currency->format($this->tax->calculate($result['price'], $result['tax_class_id'], $this->config->get('config_tax')), $this->session->data['currency']);
							} else {
								$price = false;
							}

							if ((float)$result['special']) {
								$special = $this->currency->format($this->tax->calculate($result['special'], $result['tax_class_id'], $this->config->get('config_tax')), $this->session->data['currency']);
							} else {
								$special = false;
							}

							if ($this->config->get('config_tax')) {
								$tax = $this->currency->format((float)$result['special'] ? $result['special'] : $result['price'], $this->session->data['currency']);
							} else {
								$tax = false;
							}

							if ($this->config->get('config_review_status')) {
								$rating = $result['rating'];
							} else {
								$rating = false;
							}

							$products[] = array(
								'product_id'  => $result['product_id'],
								'thumb'       => $image,
								'additional_image'	=> $additional_image,
								'name'        => $result['name'],
								'description' => utf8_substr(trim(strip_tags(html_entity_decode($result['description'], ENT_QUOTES, 'UTF-8'))), 0, $this->config->get('theme_' . $this->config->get('config_theme') . '_product_description_length')) . '..',
								'price'       => $price,
								'special'     => $special,
								'tax'         => $tax,
								'rating'      => $rating,
								'href'        => $this->url->link('product/product', 'product_id=' . $result['product_id'])
							);
						}

						break;

					case 'bestseller_products':
						$results = $this->model_catalog_product->getBestSellerProducts($setting['limit']);

						foreach ($results as $result) {
							if ($result['image']) {
								$image = $this->model_tool_image->resize($result['image'], $setting['width'], $setting['height']);
							} else {
								$image = $this->model_tool_image->resize('placeholder.png', $setting['width'], $setting['height']);
							}

							$additional_image_row = $this->model_catalog_jade_circlet->getProductAdditionalFirstImage($result['product_id']);

							if (!empty($additional_image_row['image'])) {
								$additional_image = $this->model_tool_image->resize($additional_image_row['image'], $setting['width'], $setting['height']);
							} else {
								$additional_image = '';
							}

							if ($this->customer->isLogged() || !$this->config->get('config_customer_price')) {
								$price = $this->currency->format($this->tax->calculate($result['price'], $result['tax_class_id'], $this->config->get('config_tax')), $this->session->data['currency']);
							} else {
								$price = false;
							}

							if ((float)$result['special']) {
								$special = $this->currency->format($this->tax->calculate($result['special'], $result['tax_class_id'], $this->config->get('config_tax')), $this->session->data['currency']);
							} else {
								$special = false;
							}

							if ($this->config->get('config_tax')) {
								$tax = $this->currency->format((float)$result['special'] ? $result['special'] : $result['price'], $this->session->data['currency']);
							} else {
								$tax = false;
							}

							if ($this->config->get('config_review_status')) {
								$rating = $result['rating'];
							} else {
								$rating = false;
							}

							$products[] = array(
								'product_id'  => $result['product_id'],
								'thumb'       => $image,
								'additional_image'	=> $additional_image,
								'name'        => $result['name'],
								'description' => utf8_substr(trim(strip_tags(html_entity_decode($result['description'], ENT_QUOTES, 'UTF-8'))), 0, $this->config->get('theme_' . $this->config->get('config_theme') . '_product_description_length')) . '..',
								'price'       => $price,
								'special'     => $special,
								'tax'         => $tax,
								'rating'      => $rating,
								'href'        => $this->url->link('product/product', 'product_id=' . $result['product_id'])
							);
						}
						break;

					case 'special_products':
					$special_filter_data = array(
							'sort'  => 'pd.name',
							'order' => 'ASC',
							'start' => 0,
							'limit' => $setting['limit']
						);

						$results = $this->model_catalog_product->getProductSpecials($special_filter_data);

						foreach ($results as $result) {
							if ($result['image']) {
								$image = $this->model_tool_image->resize($result['image'], $setting['width'], $setting['height']);
							} else {
								$image = $this->model_tool_image->resize('placeholder.png', $setting['width'], $setting['height']);
							}

							$additional_image_row = $this->model_catalog_jade_circlet->getProductAdditionalFirstImage($result['product_id']);

							if (!empty($additional_image_row['image'])) {
								$additional_image = $this->model_tool_image->resize($additional_image_row['image'], $setting['width'], $setting['height']);
							} else {
								$additional_image = '';
							}

							if ($this->customer->isLogged() || !$this->config->get('config_customer_price')) {
								$price = $this->currency->format($this->tax->calculate($result['price'], $result['tax_class_id'], $this->config->get('config_tax')), $this->session->data['currency']);
							} else {
								$price = false;
							}

							if ((float)$result['special']) {
								$special = $this->currency->format($this->tax->calculate($result['special'], $result['tax_class_id'], $this->config->get('config_tax')), $this->session->data['currency']);
							} else {
								$special = false;
							}

							if ($this->config->get('config_tax')) {
								$tax = $this->currency->format((float)$result['special'] ? $result['special'] : $result['price'], $this->session->data['currency']);
							} else {
								$tax = false;
							}

							if ($this->config->get('config_review_status')) {
								$rating = $result['rating'];
							} else {
								$rating = false;
							}

							$products[] = array(
								'product_id'  => $result['product_id'],
								'thumb'       => $image,
								'additional_image'	=> $additional_image,
								'name'        => $result['name'],
								'description' => utf8_substr(trim(strip_tags(html_entity_decode($result['description'], ENT_QUOTES, 'UTF-8'))), 0, $this->config->get('theme_' . $this->config->get('config_theme') . '_product_description_length')) . '..',
								'price'       => $price,
								'special'     => $special,
								'tax'         => $tax,
								'rating'      => $rating,
								'href'        => $this->url->link('product/product', 'product_id=' . $result['product_id'])
							);
						}
						break;
				}

				$data['columns'][] = array(
					'title' 				=> isset($column['description'][$this->config->get('config_language_id')]['title']) ? $column['description'][$this->config->get('config_language_id')]['title'] : '',
					'size' 					=> $column['size'],
					'module_type' 			=> $column['module_type'],
					'products' 				=> $products,
					'count' 				=> $count,
				);

				$count++;
			}
		}

		$data['module'] = $module++;

		return $this->load->view('extension/module/multi_module', $data);
	}
}