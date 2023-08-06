<?php
class ModelExtensionJadeFooter extends Model {
	public function getJadeCustomfooters($data = array()) {
		$sql = "SELECT * FROM " . DB_PREFIX . "jade_customfooter jc LEFT JOIN " . DB_PREFIX . "jade_customfooter_description jcd ON (jc.jade_customfooter_id = jcd.jade_customfooter_id) LEFT JOIN " . DB_PREFIX . "jade_customfooter_store jc2s ON (jc.jade_customfooter_id = jc2s.jade_customfooter_id) LEFT JOIN " . DB_PREFIX . "jade_customfooter_customer_group jc2cg ON (jc.jade_customfooter_id = jc2cg.jade_customfooter_id) WHERE jcd.language_id = '" . (int)$this->config->get('config_language_id') . "' AND jc.status = '1' AND jc2s.store_id = '" . (int)$this->config->get('config_store_id') . "' AND jc2cg.customer_group_id = '" . (int)$this->config->get('config_customer_group_id') . "' ORDER BY jc.sort_order ASC ";

		$query = $this->db->query($sql);

		return $query->rows;
	}

	public function addNewsletterEmail($email) {
		$this->db->query("INSERT INTO " . DB_PREFIX . "jade_customfooter_newsletter SET email = '" . $this->db->escape(utf8_strtolower($email)) . "', store_id = '". $this->config->get('config_store_id') ."', language_id = '". $this->config->get('config_language_id') ."', ip = '". $this->db->escape($this->request->server['REMOTE_ADDR']) ."', status = '1', date_added = NOW(), date_modified = NOW()");
	}

	public function getTotalSubscribersByEmail($email) {
		$query = $this->db->query("SELECT * FROM " . DB_PREFIX . "jade_customfooter_newsletter WHERE LOWER(email) = '" . $this->db->escape(utf8_strtolower($email)) . "'");

		return $query->row;
	}
}