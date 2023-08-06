<?php
class ControllerExtensionModuleTopProducts extends Controller {
	public function index($setting) {
		if ($this->config->get('config_theme') == 'default') {
			$theme = $this->config->get('theme_default_directory');
		} else {
			$theme = $this->config->get('config_theme');
		}
		if ('circlet' != $theme) {
			return;
		}

		$this->load->language('extension/module/top_products');

		$this->load->model('catalog/product');

		$this->load->model('catalog/jade_testimonial');

		$this->load->model('tool/image');

		$this->document->addStyle('catalog/view/javascript/jquery/swiper/css/swiper.min.css');
		$this->document->addStyle('catalog/view/javascript/jquery/swiper/css/opencart.css');
		$this->document->addScript('catalog/view/javascript/jquery/swiper/js/swiper.jquery.js');

		$data['products'] = array();

		if (!$setting['limit']) {
			$setting['limit'] = 4;
		}

		$data['product_status'] = isset($setting['product_status']) ? $setting['product_status'] : '';

		if (!empty($setting['product'])) {
			$products = array_slice($setting['product'], 0, (int)$setting['limit']);

			foreach ($products as $product_id) {
				$product_info = $this->model_catalog_product->getProduct($product_id);

				if ($product_info) {
					if ($product_info['image']) {
						$image = $this->model_tool_image->resize($product_info['image'], $setting['width'], $setting['height']);
					} else {
						$image = $this->model_tool_image->resize('placeholder.png', $setting['width'], $setting['height']);
					}

					if ($this->customer->isLogged() || !$this->config->get('config_customer_price')) {
						$price = $this->currency->format($this->tax->calculate($product_info['price'], $product_info['tax_class_id'], $this->config->get('config_tax')), $this->session->data['currency']);
					} else {
						$price = false;
					}

					if ((float)$product_info['special']) {
						$special = $this->currency->format($this->tax->calculate($product_info['special'], $product_info['tax_class_id'], $this->config->get('config_tax')), $this->session->data['currency']);
					} else {
						$special = false;
					}

					if ($this->config->get('config_tax')) {
						$tax = $this->currency->format((float)$product_info['special'] ? $product_info['special'] : $product_info['price'], $this->session->data['currency']);
					} else {
						$tax = false;
					}

					if ($this->config->get('config_review_status')) {
						$rating = $product_info['rating'];
					} else {
						$rating = false;
					}

					$data['products'][] = array(
						'product_id'  => $product_info['product_id'],
						'thumb'       => $image,
						'name'        => $product_info['name'],
						'description' => utf8_substr(strip_tags(html_entity_decode($product_info['description'], ENT_QUOTES, 'UTF-8')), 0, $this->config->get('theme_' . $this->config->get('config_theme') . '_product_description_length')) . '..',
						'price'       => $price,
						'special'     => $special,
						'tax'         => $tax,
						'rating'      => $rating,
						'href'        => $this->url->link('product/product', 'product_id=' . $product_info['product_id'])
					);
				}
			}
		}


		// Testimonials
		if (!$setting['testimonial_limit']) {
			$setting['testimonial_limit'] = 4;
		}

		$data['testimonial_status'] = isset($setting['testimonial_status']) ? $setting['testimonial_status'] : '';

		$results = $this->model_catalog_jade_testimonial->getJadeTestimonials();
		$data['jade_testimonials'] = array();
		foreach($results as $result) {
			if ($result['image']) {
				$image = $this->model_tool_image->resize($result['image'], $setting['testimonial_width'], $setting['testimonial_height']);
			} else {
				$image = $this->model_tool_image->resize('nouserpic.png', $setting['testimonial_width'], $setting['testimonial_height']);
			}

			$data['jade_testimonials'][] = array(
				'image'				=> $image,
				'author'			=> $result['author'],
				'title'				=> $result['title'],
				'destination'		=> $result['destination'],
				'description'		=> utf8_substr(strip_tags(html_entity_decode($result['description'], ENT_QUOTES, 'UTF-8')), 0, 300) . '..',
				'rating'			=> $result['rating'],
				'status'			=> $result['status'],
				'sort_order'		=> $result['sort_order'],
				'j_click'				=> $this->url->link('extension/module/top_products/info', 'jade_testimonial_id=' . $result['jade_testimonial_id'] . '&testimonial_width='. $setting['testimonial_width'] . '&testimonial_height='. $setting['testimonial_height'], true),
			);
		}

		$data['product_class'] = 'col-md-12';
		$data['testimonial_class'] = 'col-md-12';

		if(($data['product_status'] && $data['products']) && ($data['testimonial_status'] && $data['jade_testimonials'])) {
			$data['product_class'] = 'col-md-8';
			$data['testimonial_class'] = 'col-md-4';
		}

		if(($data['product_status'] && $data['products']) || ($data['testimonial_status'] && $data['jade_testimonials'])) {
			return $this->load->view('extension/module/top_products', $data);
		}
	}

	public function info() {
		$this->load->model('catalog/jade_testimonial');
		$this->load->model('tool/image');

		if (isset($this->request->get['jade_testimonial_id'])) {
			$jade_testimonial_id = (int)$this->request->get['jade_testimonial_id'];
		} else {
			$jade_testimonial_id = 0;
		}

		if (isset($this->request->get['testimonial_width'])) {
			$testimonial_width = (int)$this->request->get['testimonial_width'];
		} else {
			$testimonial_width = 120;
		}

		if (isset($this->request->get['testimonial_height'])) {
			$testimonial_height = (int)$this->request->get['testimonial_height'];
		} else {
			$testimonial_height = 120;
		}

		$json = array();

		$jade_testimonial_info = $this->model_catalog_jade_testimonial->getJadeTestimonial($jade_testimonial_id);

		if ($jade_testimonial_info) {
			if ($jade_testimonial_info['image']) {
				$image = $this->model_tool_image->resize($jade_testimonial_info['image'], $testimonial_width, $testimonial_height);
			} else {
				$image = $this->model_tool_image->resize('nouserpic.png', $testimonial_width, $testimonial_height);
			}

			$json = array(
				'image'				=> $image,
				'author'			=> $jade_testimonial_info['author'],
				'title'				=> $jade_testimonial_info['title'],
				'destination'		=> $jade_testimonial_info['destination'],
				'description'		=> html_entity_decode($jade_testimonial_info['description'], ENT_QUOTES, 'UTF-8'),
				'rating'			=> $jade_testimonial_info['rating'],
			);
		}

		$this->response->addHeader('Content-Type: application/json');
		$this->response->setOutput(json_encode($json));
	}
}