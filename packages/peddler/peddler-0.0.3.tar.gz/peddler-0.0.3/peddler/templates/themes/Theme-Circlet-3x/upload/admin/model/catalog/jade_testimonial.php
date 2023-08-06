<?php
class ModelCatalogJadeTestimonial extends Model {
	public function addJadeTestimonial($data) {
		$this->db->query("INSERT INTO " . DB_PREFIX . "jade_testimonial SET sort_order = '" . (int)$data['sort_order'] . "', status = '" . (int)$data['status'] . "', rating = '" . (int)$data['rating'] . "', author = '" . $this->db->escape($data['author']) . "', image = '" . $this->db->escape($data['image']) . "', date_added = NOW()");

		$jade_testimonial_id = $this->db->getLastId();

		foreach ($data['jade_testimonial_description'] as $language_id => $value) {
			$this->db->query("INSERT INTO " . DB_PREFIX . "jade_testimonial_description SET jade_testimonial_id = '" . (int)$jade_testimonial_id . "', language_id = '" . (int)$language_id . "', title = '" . $this->db->escape($value['title']) . "', description = '" . $this->db->escape($value['description']) . "', destination = '" . $this->db->escape($value['destination']) . "'");
		}

		return $jade_testimonial_id;
	}

	public function editJadeTestimonial($jade_testimonial_id, $data) {
		$this->db->query("UPDATE " . DB_PREFIX . "jade_testimonial SET sort_order = '" . (int)$data['sort_order'] . "', status = '" . (int)$data['status'] . "', rating = '" . (int)$data['rating'] . "', author = '" . $this->db->escape($data['author']) . "', image = '" . $this->db->escape($data['image']) . "' WHERE jade_testimonial_id = '" . (int)$jade_testimonial_id . "'");

		$this->db->query("DELETE FROM " . DB_PREFIX . "jade_testimonial_description WHERE jade_testimonial_id = '" . (int)$jade_testimonial_id . "'");

		foreach ($data['jade_testimonial_description'] as $language_id => $value) {
			$this->db->query("INSERT INTO " . DB_PREFIX . "jade_testimonial_description SET jade_testimonial_id = '" . (int)$jade_testimonial_id . "', language_id = '" . (int)$language_id . "', title = '" . $this->db->escape($value['title']) . "', description = '" . $this->db->escape($value['description']) . "', destination = '" . $this->db->escape($value['destination']) . "'");
		}
	}

	public function deleteJadeTestimonial($jade_testimonial_id) {
		$this->db->query("DELETE FROM " . DB_PREFIX . "jade_testimonial WHERE jade_testimonial_id = '" . (int)$jade_testimonial_id . "'");
		$this->db->query("DELETE FROM " . DB_PREFIX . "jade_testimonial_description WHERE jade_testimonial_id = '" . (int)$jade_testimonial_id . "'");
	}

	public function getJadeTestimonial($jade_testimonial_id) {
		$query = $this->db->query("SELECT DISTINCT * FROM " . DB_PREFIX . "jade_testimonial WHERE jade_testimonial_id = '" . (int)$jade_testimonial_id . "'");

		return $query->row;
	}

	public function getJadeTestimonials($data = array()) {
		$sql = "SELECT * FROM " . DB_PREFIX . "jade_testimonial t LEFT JOIN " . DB_PREFIX . "jade_testimonial_description td ON (t.jade_testimonial_id = td.jade_testimonial_id) WHERE td.language_id = '" . (int)$this->config->get('config_language_id') . "'";

		$sort_data = array(
			'td.title',
			'td.destination',
			't.author',
			't.sort_order',
			't.date_added',
		);

		if (isset($data['sort']) && in_array($data['sort'], $sort_data)) {
			$sql .= " ORDER BY " . $data['sort'];
		} else {
			$sql .= " ORDER BY td.title";
		}

		if (isset($data['order']) && ($data['order'] == 'DESC')) {
			$sql .= " DESC";
		} else {
			$sql .= " ASC";
		}

		if (isset($data['start']) || isset($data['limit'])) {
			if ($data['start'] < 0) {
				$data['start'] = 0;
			}

			if ($data['limit'] < 1) {
				$data['limit'] = 20;
			}

			$sql .= " LIMIT " . (int)$data['start'] . "," . (int)$data['limit'];
		}

		$query = $this->db->query($sql);

		return $query->rows;
	}

	public function getJadeTestimonialDescriptions($jade_testimonial_id) {
		$jade_testimonial_description_data = array();

		$query = $this->db->query("SELECT * FROM " . DB_PREFIX . "jade_testimonial_description WHERE jade_testimonial_id = '" . (int)$jade_testimonial_id . "'");

		foreach ($query->rows as $result) {
			$jade_testimonial_description_data[$result['language_id']] = array(
				'title'            => $result['title'],
				'description'      => $result['description'],
				'destination'      => $result['destination'],
			);
		}

		return $jade_testimonial_description_data;
	}

	public function getTotalJadeTestimonials() {
		$query = $this->db->query("SELECT COUNT(*) AS total FROM " . DB_PREFIX . "jade_testimonial");

		return $query->row['total'];
	}

	public function create__Jade__Testimonial__Tables() {
		$this->db->query("CREATE TABLE IF NOT EXISTS `" . DB_PREFIX . "jade_testimonial` (`jade_testimonial_id` int(11) NOT NULL AUTO_INCREMENT,`author` varchar(255) NOT NULL,`image` varchar(255) NOT NULL,`rating` int(11) NOT NULL,`status` tinyint(4) NOT NULL,`sort_order` int(11) NOT NULL,`date_added` date NOT NULL,PRIMARY KEY (`jade_testimonial_id`)) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0");

		$this->db->query("CREATE TABLE IF NOT EXISTS `" . DB_PREFIX . "jade_testimonial_description` (`jade_testimonial_id` int(11) NOT NULL,`language_id` int(11) NOT NULL,`destination` varchar(255) NOT NULL,`title` varchar(255) NOT NULL,`description` text NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;");
	}
}