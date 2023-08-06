<?php
class ModelCatalogJadeTestimonial extends Model {
	public function getJadeTestimonials($data = array()) {
		$sql = "SELECT * FROM " . DB_PREFIX . "jade_testimonial t LEFT JOIN " . DB_PREFIX . "jade_testimonial_description td ON (t.jade_testimonial_id = td.jade_testimonial_id) WHERE td.language_id = '" . (int)$this->config->get('config_language_id') . "' AND t.status = 1 ORDER BY t.sort_order ASC";

		$query = $this->db->query($sql);

		return $query->rows;
	}

	public function getJadeTestimonial($jade_testimonial_id) {
		$sql = "SELECT * FROM " . DB_PREFIX . "jade_testimonial t LEFT JOIN " . DB_PREFIX . "jade_testimonial_description td ON (t.jade_testimonial_id = td.jade_testimonial_id) WHERE td.language_id = '" . (int)$this->config->get('config_language_id') . "' AND t.status = 1  AND t.jade_testimonial_id = '". (int)$jade_testimonial_id ."'";

		$query = $this->db->query($sql);

		return $query->row;
	}
}